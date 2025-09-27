"""Build Language/Dialect models from a local Glottolog checkout.

- Exports ALL languages and their dialects (no historic filtering).
- Does not map any values into Language.sources or Dialect.sources.
- Preserves optional Newick generation for root languages only.

Usage:
  python build_glottolog_models.py --glottolog ~/code/glottolog/ --out glottolog.json
"""

from __future__ import annotations

import argparse
import configparser
import json
import re
import subprocess
from dataclasses import dataclass, field as dc_field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Final, List, Optional

from pydantic import AnyUrl, TypeAdapter

from cltk.core.data_types import *

# -------------------- Internal helpers --------------------


@dataclass
class RawNode:
    """Minimal storage of parsed md.ini + filesystem info before Pydantic conversion."""

    glottocode: str
    path: Path
    parent_glottocode: Optional[str]
    level: Level
    core: Dict[str, Any]
    altnames: Dict[str, List[str]]
    links: Dict[str, str]
    sources: List[str]
    children: List[str] = dc_field(default_factory=list)


TIMESPAN_PAT = re.compile(r"^\s*(-?\d+)\s*[-/]\s*(-?\d+)\s*$")


def parse_timespan(raw: Optional[str]) -> Timespan | None:
    if not raw:
        return None
    m = TIMESPAN_PAT.match(raw.strip())
    if m:
        return Timespan(start=int(m.group(1)), end=int(m.group(2)), note=raw)
    return Timespan(note=raw)


def split_lines(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [x.strip() for x in raw.splitlines() if x.strip()]


def as_status(raw: Optional[str]) -> Status:
    s = (raw or "").strip().lower()
    mapping: Final[dict[str, Status]] = {
        "living": "living",
        "extinct": "extinct",
        "second language only": "second language only",
        "artificial": "artificial",
        "unattested": "unattested",
        "unknown": "unknown",
    }
    return mapping.get(s, "unknown")


def safe_float(x: Optional[str]) -> Optional[float]:
    try:
        return float(x) if x not in (None, "", "None") else None
    except Exception:
        return None


def find_md_ini_dirs(root: Path) -> List[Path]:
    return [p for p in root.rglob("md.ini")]


def read_md_ini(p: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(p, encoding="utf-8")
    return cfg


def parent_glottocode_from_path(md_path: Path, tree_root: Path) -> Optional[str]:
    this_dir = md_path.parent
    if this_dir == tree_root:
        return None
    parent_dir = this_dir.parent
    if parent_dir == tree_root:
        return None
    return parent_dir.name


def glottocode_from_path(md_path: Path) -> str:
    return md_path.parent.name


# --- Repo provenance readers -------------------------------------------


def read_glottolog_version(repo_root: Path) -> Optional[str]:
    ini_path = repo_root / "glottolog.ini"
    if not ini_path.exists():
        return None
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(ini_path, encoding="utf-8")
    for section in cfg.sections():
        for key in ("version", "release"):
            if cfg.has_option(section, key):
                val = cfg.get(section, key).strip()
                if val:
                    return val
    return None


def run_git(cmd: list[str], cwd: Path) -> Optional[str]:
    try:
        out = subprocess.check_output(
            cmd, cwd=str(cwd), stderr=subprocess.DEVNULL, text=True
        ).strip()
        return out if out else None
    except Exception:
        return None


def read_git_provenance(repo_root: Path) -> tuple[Optional[str], Optional[date]]:
    """Returns (commit_sha, commit_date) if repo_root is a git checkout; otherwise (None, None)."""
    sha = run_git(["git", "rev-parse", "HEAD"], cwd=repo_root)
    iso = run_git(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=repo_root)
    d: Optional[date] = None
    if iso:
        try:
            d = datetime.fromisoformat(iso.replace("Z", "+00:00")).date()
        except Exception:
            d = None
    return sha, d


# -------------------- Parse entire tree into RawNodes --------------------


def build_raw_nodes(tree_root: Path) -> Dict[str, RawNode]:
    nodes: Dict[str, RawNode] = {}

    for md in find_md_ini_dirs(tree_root):
        cfg = read_md_ini(md)
        core = dict(cfg["core"]) if cfg.has_section("core") else {}

        lvl = core.get("level", "").strip().lower()
        if lvl not in ("family", "language", "dialect"):
            lvl = "language"

        altnames: Dict[str, List[str]] = {}
        if cfg.has_section("altnames"):
            for k, v in cfg.items("altnames"):
                altnames[k] = split_lines(v)

        links: Dict[str, str] = {}
        if cfg.has_section("links"):
            for k, v in cfg.items("links"):
                v = v.strip()
                if v:
                    links[k] = v

        # Do not parse sources; we never map them into Language/Dialect
        sources: List[str] = []

        gcode = glottocode_from_path(md)
        parent_g = parent_glottocode_from_path(md, tree_root)

        nodes[gcode] = RawNode(
            glottocode=gcode,
            path=md.parent,
            parent_glottocode=parent_g,
            level=lvl,  # type: ignore
            core=core,
            altnames=altnames,
            links=links,
            sources=sources,
        )

    # fill children
    for g, node in nodes.items():
        pg = node.parent_glottocode
        if pg and pg in nodes:
            nodes[pg].children.append(g)

    return nodes


# -------------------- Convert RawNodes -> Language/Dialect --------------------


def parse_macroareas(raw: Optional[str]) -> List[Macroarea]:
    items = split_lines(raw)
    out: List[Macroarea] = []
    for x in items:
        cap = x.strip().capitalize()
        if cap in {
            "Africa",
            "Eurasia",
            "Papunesia",
            "Australia",
            "North america",
            "South america",
            "Antarctica",
        }:
            if cap == "North america":
                cap = "North America"
            if cap == "South america":
                cap = "South America"
            out.append(cap)  # type: ignore
    return out


def parse_countries(raw: Optional[str]) -> List[str]:
    items = split_lines(raw)
    return [x.strip().upper() for x in items if re.fullmatch(r"[A-Za-z]{2}", x.strip())]


def build_geo(core: Dict[str, Any]) -> Optional[GeoArea]:
    lat = safe_float(core.get("latitude"))
    lon = safe_float(core.get("longitude"))
    centroid = (
        GeoPoint(lat=lat, lon=lon) if (lat is not None and lon is not None) else None
    )
    macs = parse_macroareas(core.get("macroareas"))
    ctries = parse_countries(core.get("countries"))
    if not centroid and not macs and not ctries:
        return None
    return GeoArea(centroid=centroid, macroareas=macs, countries=ctries)


def build_identifiers(core: Dict[str, Any], glottocode: str) -> List[Identifier]:
    ids: List[Identifier] = [Identifier(scheme="glottocode", value=glottocode)]
    for k, scheme in (
        ("iso639-3", "639-3"),
        ("iso639-2", "639-2"),
        ("iso639-1", "639-1"),
        ("hid", "639-3"),
    ):
        v = core.get(k)
        if v and v.strip().lower() != "none":
            ids.append(Identifier(scheme=f"iso{scheme}", value=v.strip()))
    return ids


def build_iso_set(core: Dict[str, Any]) -> Dict[ISOType, str]:
    out: Dict[ISOType, str] = {}
    for lit, key in (
        ("639-1", "iso639-1"),
        ("639-2", "iso639-2"),
        ("639-3", "iso639-3"),
    ):
        v = core.get(key)
        if v and v.strip().lower() != "none":
            out[lit] = v.strip()  # type: ignore
    return out


def build_alt_names(altnames: Dict[str, List[str]]) -> List[NameVariant]:
    out: List[NameVariant] = []
    for source, vals in altnames.items():
        for v in vals:
            if v:
                out.append(NameVariant(value=v, source=source))
    return out


def build_links(links: Dict[str, str]) -> List[Link]:
    out: List[Link] = []
    ta = TypeAdapter(AnyUrl)
    for title, url in links.items():
        try:
            parsed_url: AnyUrl = ta.validate_python(url)
            out.append(Link(title=title, url=parsed_url))
        except Exception:
            # invalid URL → skip
            pass
    return out


def raw_to_models(
    nodes: Dict[str, RawNode],
    root_glottocode: Optional[str] = None,
    historic_cutoff: Optional[int] = None,  # kept for CLI compatibility; ignored
) -> Dict[str, Language]:
    """Convert the raw graph to Language/Dialect objects.

    - Materializes ALL languages (level == 'language').
    - Attaches ALL dialects to their nearest language ancestor.
    - Families are not materialized.
    - `historic_cutoff` is ignored (kept for backward compatibility).
    """

    def lineage_of(g: str) -> List[str]:
        lin: List[str] = []
        cur = g
        seen = set()
        while True:
            node = nodes.get(cur)
            if not node:
                break
            pg = node.parent_glottocode
            if not pg:
                break
            if pg in seen:
                break
            lin.append(pg)
            seen.add(pg)
            cur = pg
        return list(reversed(lin))

    if root_glottocode and root_glottocode in nodes:
        allowed = set()
        queue = [root_glottocode]
        while queue:
            cur = queue.pop(0)
            if cur in allowed:
                continue
            allowed.add(cur)
            queue.extend(nodes[cur].children)
    else:
        allowed = set(nodes.keys())

    langs: Dict[str, Language] = {}
    pending_dialects_by_parent: Dict[str, List[Dialect]] = {}

    for g, rn in nodes.items():
        if g not in allowed:
            continue

        core = rn.core
        name = core.get("name", g)
        status = as_status(core.get("status"))
        geo = build_geo(core)
        timespan = parse_timespan(core.get("timespan"))
        identifiers = build_identifiers(core, g)
        iso_set = build_iso_set(core)
        iso = iso_set.get("639-3") or core.get("iso639-3")
        alt_names = build_alt_names(rn.altnames)
        links = build_links(rn.links)

        parent = rn.parent_glottocode if rn.parent_glottocode in allowed else None
        lineage = [x for x in lineage_of(g) if x in allowed]
        children = [c for c in rn.children if c in allowed]

        scripts: List[str] = []
        orthographies: List[Orthography] = []

        if rn.level == "language":
            # Materialize ALL languages
            lang = Language(
                name=name,
                glottolog_id=g,
                identifiers=identifiers,
                level=rn.level,  # type: ignore
                status=status,
                type=core.get("type"),
                geo=geo,
                timespan=timespan,
                classification=Classification(
                    level=rn.level,  # type: ignore
                    parent_glottocode=parent,
                    lineage=lineage,
                    children_glottocodes=children,
                ),
                family_id=lineage[0] if lineage else None,
                parent_id=parent,
                iso=iso,
                iso_set=iso_set,
                alt_names=alt_names,
                scripts=scripts,
                orthographies=orthographies,
                # sources: intentionally omitted
                links=links,
                latitude=geo.centroid.lat if geo and geo.centroid else None,
                longitude=geo.centroid.lon if geo and geo.centroid else None,
            )
            langs[g] = lang

        elif rn.level == "dialect":
            # find nearest language ancestor
            anc = g
            parent_lang = None
            while True:
                anc_node = nodes.get(anc)
                if not anc_node:
                    break
                pg = anc_node.parent_glottocode
                if not pg:
                    break
                if pg in allowed and nodes[pg].level == "language":
                    parent_lang = pg
                    break
                anc = pg

            dia = Dialect(
                glottolog_id=g,
                language_code=g,
                name=name,
                status=status,
                alt_names=alt_names,
                identifiers=identifiers,
                geo=geo,
                timespan=timespan,
                scripts=[],
                orthographies=[],
                # sources: intentionally omitted
                links=links,
            )
            if parent_lang:
                pending_dialects_by_parent.setdefault(parent_lang, []).append(dia)

    for parent_g, dlist in pending_dialects_by_parent.items():
        if parent_g in langs:
            langs[parent_g].dialects.extend(dlist)

    # Update children lists to include only materialized languages
    for g, lang in langs.items():
        child_langs = [c for c in nodes[g].children if c in langs]
        lang.classification.children_glottocodes = child_langs

    return langs


# -------------------- Newick generation --------------------


def to_newick(glottocode: str, langs: Dict[str, Language]) -> Optional[str]:
    if glottocode not in langs:
        return None

    def label(g: str) -> str:
        nm = langs[g].name.replace(" ", "_")
        return f"{nm}[{g}]"

    def rec(g: str) -> str:
        children = langs[g].classification.children_glottocodes
        dialect_tips = []
        if langs[g].dialects:
            for d in langs[g].dialects:
                dn = d.name.replace(" ", "_")
                dialect_tips.append(f"{dn}[{d.glottolog_id}]")

        subparts = []
        for c in children:
            subparts.append(rec(c))
        subparts.extend(dialect_tips)

        if subparts:
            return f"({','.join(subparts)}){label(g)}"
        else:
            return label(g)

    return rec(glottocode) + ";"


# -------------------- Main CLI --------------------


def main():
    ap = argparse.ArgumentParser(
        description="Build Language/Dialect models from Glottolog languoids/tree (ALL languages, ALL dialects)."
    )
    ap.add_argument(
        "--glottolog",
        required=True,
        help="Path to local glottolog checkout (repo root).",
    )
    ap.add_argument(
        "--root",
        help="Optional root glottocode to restrict export to a subtree (e.g., indo1319).",
    )
    ap.add_argument("--out", required=True, help="Output JSON file.")
    ap.add_argument(
        "--emit-newick",
        action="store_true",
        help="If set, computes .newick for the chosen root node(s).",
    )
    # kept for backward compatibility; ignored
    ap.add_argument(
        "--historic-cutoff",
        type=int,
        default=1700,
        help="Deprecated/ignored. All languages and dialects are exported.",
    )
    args = ap.parse_args()

    repo_root = Path(args.glottolog).expanduser().resolve()
    tree_root = repo_root / "languoids" / "tree"
    if not tree_root.exists():
        raise SystemExit(
            f"Cannot find {tree_root}. Are you sure --glottolog points to the repo root?"
        )

    # Provenance
    gl_version = read_glottolog_version(repo_root)
    commit_sha, commit_date = read_git_provenance(repo_root)
    fallback_today = date.today()
    print(f"Glottolog version: {gl_version or '(unknown)'}")
    print(f"Git commit: {commit_sha or '(none)'}")
    print(f"Commit date: {commit_date or fallback_today}")

    print("Scanning languoids/tree ...")
    raw = build_raw_nodes(tree_root)
    print(f"Parsed {len(raw)} md.ini files.")

    print("Converting to models (all languages and dialects) ...")
    langs = raw_to_models(
        raw,
        root_glottocode=args.root,
        historic_cutoff=None,  # ignored
    )
    lang_count = len(langs)
    dia_count = sum(len(L.dialects) for L in langs.values())
    print(f"Materialized {lang_count} languages and {dia_count} dialects.")

    # Determine root languages for optional Newick
    if args.root:
        roots = [args.root] if args.root in langs else []
    else:
        roots = [
            g
            for g, L in langs.items()
            if (
                L.classification.parent_glottocode is None
                or L.classification.parent_glottocode not in langs
            )
        ]

    # Optional Newick for each root
    if args.emit_newick:
        for r in roots:
            nw = to_newick(r, langs)
            if nw:
                langs[r].newick = nw

    # Apply provenance to all languages
    for L in langs.values():
        L.glottolog_version = gl_version
        L.commit_sha = commit_sha
        L.last_updated = commit_date or fallback_today

    # Serialize ALL languages (each includes its dialects)
    payload = [langs[g].model_dump(mode="json") for g in sorted(langs.keys())]
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(payload)} languages (with dialects) to {out_path}")


if __name__ == "__main__":
    main()
