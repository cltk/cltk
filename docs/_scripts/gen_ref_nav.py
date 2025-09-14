from __future__ import annotations

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

# Ensure top-level Home and Reference are present in nav
nav["Home"] = "index.md"
nav["Reference"] = (REF_ROOT / "index.md").as_posix()

for dotted, src_path in iter_python_modules(PKG_ROOT):
    parts = dotted.split(".")
    if parts[0] != "cltk":
        continue

    # Write one markdown file per module/package
    out_path = REF_ROOT.joinpath(*parts, "index.md")
    with mkdocs_gen_files.open(out_path, "w") as fd:
        fd.write(f"::: {dotted}\n")

    # Map to navigation under the "Reference" section
    nav[["Reference", *parts]] = out_path.as_posix()

    # Link to the source file for edit/view
    mkdocs_gen_files.set_edit_path(out_path, src_path)

# Write a top-level reference index if not already present
ref_index = REF_ROOT / "index.md"
if not ref_index.exists():
    with mkdocs_gen_files.open(ref_index, "w") as fd:
        fd.write("# API Reference\n\nBrowse the auto-generated API reference below.\n")

# Emit the navigation in Literate Nav format
with mkdocs_gen_files.open("SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

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
    "cltk.morphosyntax.processes.ChatGPTMorphosyntaxProcess",
    "ChatGPTMorphosyntaxProcess",
)
_write_subclasses_page(
    "cltk.dependency.processes.ChatGPTDependencyProcess",
    "ChatGPTDependencyProcess",
)
_write_subclasses_page(
    "cltk.stanza.processes.StanzaAnalyzeProcess",
    "StanzaAnalyzeProcess",
)
