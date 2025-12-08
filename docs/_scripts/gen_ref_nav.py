from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import mkdocs_gen_files

SRC_ROOT = Path("src")
PKG_ROOT = SRC_ROOT / "cltk"
REF_ROOT = Path("reference")


def iter_python_modules(root: Path):
    for path in sorted(root.rglob("*.py")):
        # Skip dunder inits at root level; we'll still expose packages
        module_path = path.relative_to(SRC_ROOT).with_suffix("")
        dotted = ".".join(module_path.parts)
        if dotted.endswith(".__init__"):
            dotted = dotted[: -len(".__init__")]
        yield dotted, path


nav = mkdocs_gen_files.Nav()
# Collect top-level subpackages to build a human-friendly Reference index
top_packages: set[str] = set()
# Track package vs module and a parent->children mapping for recursive indexes
packages_set: set[str] = set()
children: dict[str, set[str]] = defaultdict(set)

# Ensure top-level Home and Reference are present in nav
nav["Home"] = "index.md"
nav["Quickstart"] = "quickstart.md"
nav["Advanced Configuration"] = "advanced-model-configuration.md"
nav["Advanced Prompting"] = "advanced-prompting.md"
nav["Troubleshooting"] = "troubleshooting.md"

for dotted, src_path in iter_python_modules(PKG_ROOT):
    parts = dotted.split(".")
    if parts[0] != "cltk":
        continue
    if len(parts) > 1:
        top_packages.add(parts[1])

    # Track package nodes and build parent->children relationships
    if src_path.name == "__init__.py":
        packages_set.add(dotted)
    parent = ".".join(parts[:-1])
    if parent:
        children[parent].add(dotted)

    # Write one markdown file per module/package (mkdocstrings include)
    out_path = REF_ROOT.joinpath(*parts, "index.md")
    with mkdocs_gen_files.open(out_path, "w") as fd:
        fd.write(f"::: {dotted}\n")

    # Map to navigation under the "Reference" section
    nav[["Reference", *parts]] = out_path.as_posix()

    # Link to the source file for edit/view
    mkdocs_gen_files.set_edit_path(out_path, src_path)

# Write a top-level Reference index with a simple table of contents
ref_index = REF_ROOT / "index.md"
with mkdocs_gen_files.open(ref_index, "w") as fd:
    fd.write("# API Reference\n\n")
    fd.write("Browse the auto-generated API reference below.\n\n")
    if top_packages:
        fd.write("## Modules and Packages\n\n")
        for pkg in sorted(top_packages):
            fd.write(f"- [`cltk.{pkg}`](cltk/{pkg}/index.md)\n")

# Augment package pages with a recursive submodule table of contents
def _write_subtree(fd, base_parts: list[str], parent: str, level: int = 0) -> None:
    kids = sorted(children.get(parent, []))
    for k in kids:
        indent = "  " * level
        child_parts = k.split(".")
        # Compute relative path from the base package page to the child page
        tail_parts = child_parts[len(base_parts) :]
        if not tail_parts:
            # Should not happen, but guard against empty tail
            rel_path = "./index.md"
        else:
            rel_path = "/".join(tail_parts + ["index.md"])
        fd.write(f"{indent}- [`{k}`]({rel_path})\n")
        if k in packages_set:
            _write_subtree(fd, base_parts, k, level + 1)

for pkg in sorted(packages_set):
    parts = pkg.split(".")
    out_path = REF_ROOT.joinpath(*parts, "index.md")
    # Re-write the package page to include mkdocstrings include and a TOC
    with mkdocs_gen_files.open(out_path, "w") as fd:
        fd.write(f"# `{pkg}`\n\n")
        fd.write(f"::: {pkg}\n\n")
        # Only add contents if there are children
        if children.get(pkg):
            fd.write("## Submodules\n\n")
            _write_subtree(fd, parts, pkg, 0)


# --- Add subclass indexes for key base/process classes -----------------------

def _collect_subclasses(cls: type) -> list[type]:
    seen: set[type] = set()
    def _walk(c: type) -> None:
        for sub in c.__subclasses__():
            if sub in seen:
                continue
            seen.add(sub)
            _walk(sub)
    _walk(cls)
    # Stable order by qualified name
    return sorted(seen, key=lambda c: f"{c.__module__}.{c.__qualname__}")


def _write_subclasses_page(dotted_class: str, title: str) -> None:
    parts = dotted_class.split(".")
    mod_name = ".".join(parts[:-1])
    cls_name = parts[-1]
    try:
        mod = __import__(mod_name, fromlist=[cls_name])
        base_cls = getattr(mod, cls_name)
    except Exception:
        return
    subs = _collect_subclasses(base_cls)
    # Build page only if there are discovered subclasses
    out_path = REF_ROOT.joinpath(*parts, "subclasses.md")
    with mkdocs_gen_files.open(out_path, "w") as fd:
        fd.write(f"# {title}: Subclasses\n\n")
        if not subs:
            fd.write("No subclasses discovered.\n")
        else:
            for sub in subs:
                dotted = f"{sub.__module__}.{sub.__qualname__}"
                fd.write(f"- `{dotted}`\n")
    # Add to nav under the class node
    nav[["Reference", *parts, "Subclasses"]] = out_path.as_posix()


# Generate subclass listings for selected bases
_write_subclasses_page(
    "cltk.morphosyntax.processes.GenAIMorphosyntaxProcess",
    "GenAIMorphosyntaxProcess",
)
_write_subclasses_page(
    "cltk.dependency.processes.GenAIDependencyProcess",
    "GenAIDependencyProcess",
)
_write_subclasses_page(
    "cltk.stanza.processes.StanzaAnalyzeProcess",
    "StanzaAnalyzeProcess",
)

# Emit the navigation in Literate Nav format (after adding subclass pages and Reference index)
with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
