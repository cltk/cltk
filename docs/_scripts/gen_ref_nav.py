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
