> Warning: This is an alpha feature. APIs and behaviors may change; use in production with care.

## Examples

```bash
cltk analyze --lang lati1261 --backend stanza --out conllu --text "Gallia est omnis divisa..." > out.conllu
```

```bash
cltk analyze --lang grc --backend openai --out readers-guide --text-file input.txt --out-file guide.md
```

```bash
cltk compare --lang grc --text-file input.txt --backends stanza,openai --out-dir reports/ --basename plato_apology
```

```bash
cltk export --lang grc --backend stanza --text-file input.txt --parquet out.parquet
```

## Notes

- Stdout redirection is supported for single-output commands; use `> out.file` to capture results.
- Batch mode: use `--input-dir` with `--out-dir` and optional `--glob` to process a directory and preserve subdirectories.
