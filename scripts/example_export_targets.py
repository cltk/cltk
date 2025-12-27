"""Example script for scholar-facing export targets."""

from cltk import NLP
from cltk.exports import (
    doc_to_igt_html,
    doc_to_igt_latex,
    doc_to_readers_guide_html,
    doc_to_tei_xml,
)


def main() -> None:
    text = "Gallia est omnis divisa in partes tres."
    nlp = NLP(language_code="lat", backend="openai")
    doc = nlp.analyze(text)

    igt_latex: str = doc_to_igt_latex(doc)
    with open("scripts/example_igt.tex", "w") as f:
        f.write(igt_latex)
    print("IGT LaTeX written to scripts/example_igt.tex")

    igt_html: str = doc_to_igt_html(doc)
    with open("scripts/example_igt.html", "w") as f:
        f.write(igt_html)
    print("IGT HTML written to scripts/example_igt.html")

    tei: str = doc_to_tei_xml(doc)
    with open("scripts/example_tei.xml", "w") as f:
        f.write(tei)
    print("TEI XML written to scripts/example_tei.xml")

    readers: str = doc_to_readers_guide_html(doc)
    with open("scripts/example_readers.html", "w") as f:
        f.write(readers)
    print("Reader's Guide HTML written to scripts/example_readers.html")


if __name__ == "__main__":
    main()
