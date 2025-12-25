from cltk.evaluation.compare_backends import compare_backends, report_to_markdown


def main() -> None:
    report = compare_backends(
        "lati1261",
        "Gallia est omnis divisa in partes tres.",
        ["stanza", "openai", "mistral", "ollama"],
    )
    print(report_to_markdown(report))

    with open("evaluation/comparison_report.md", "w") as f:
        f.write(report_to_markdown(report))


if __name__ == "__main__":
    main()
