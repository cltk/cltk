"""Compare all available backends and return a report."""

from cltk.evaluation.compare_backends import compare_backends, report_to_markdown


def main(lang_code: str, text: str) -> None:
    report = compare_backends(
        lang_code,
        text,
        [
            "stanza",
            "openai",
            #  "mistral",
            #  "ollama"
        ],
    )
    print(report_to_markdown(report))

    with open(f"evaluation/comparison_report_{lang_code}.md", "w") as f:
        f.write(report_to_markdown(report))


if __name__ == "__main__":
    LANGS: list[tuple[str, str]] = [
        ("lati1261", "Gallia est omnis divisa in partes tres."),
        (
            "anci1242",
            "Δαρείου καὶ Παρυσάτιδος γίγνονται παῖδες δύο, πρεσβύτερος μὲν Ἀρταξέρξης, νεώτερος δὲ Κῦρος: ἐπεὶ δὲ ἠσθένει Δαρεῖος καὶ ὑπώπτευε τελευτὴν τοῦ βίου, ἐβούλετο τὼ παῖδε ἀμφοτέρω παρεῖναι.",
        ),
    ]
    for LANG_CODE, TEXT in LANGS:
        main(lang_code=LANG_CODE, text=TEXT)
