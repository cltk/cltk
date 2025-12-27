"""Example using `tlg-indices` package to convert TLG corpus and clean text."""

import os
import pickle

import pandas as pd  # type: ignore[import-untyped]
import pyarrow as pa  # type: ignore[import-untyped]
import pyarrow.csv as pacsv  # type: ignore[import-untyped]
import pyarrow.feather as feather  # type: ignore[import-untyped]
from tlg_indices.file_utils import (  # type: ignore[import-not-found, unused-ignore]
    assemble_tlg_works_filepaths,  # noqa: F401
    assemble_tlg_works_filepaths_for_author,
)
from tlg_indices.text_cleaning import (
    tlg_plaintext_cleanup,  # type: ignore[import-not-found, unused-ignore]
)
from tlg_indices.tlgu import (
    tlgu_convert_corpus,  # type: ignore[import-not-found, unused-ignore]
)

from cltk import NLP
from cltk.core.data_types import BACKEND_TYPES
from cltk.utils.file_outputs import (
    doc_to_conllu,
    doc_to_feature_table,
    format_readers_guide,
)

backend: BACKEND_TYPES = "stanza"  # or "openai", "ollama", "mistral"
nlp_grc: NLP = NLP(language_code="anci1242", backend=backend)

# Convert entire TLG corpus into author files
conveted_tlg_dir: str = "~/Downloads/tlg-works"
if not os.path.exists(os.path.expanduser(conveted_tlg_dir)):
    # `Requires `tlg-indices` package: `pip install tlg-indices`
    tlgu_convert_corpus(
        orig_txt_dir="~/tlg/TLG_E",
        target_txt_dir=conveted_tlg_dir,
        corpus="tlg",
        grouping="work",
    )

# Get filepaths of converted TLG works
# tlg_works_filepaths: list[str] = assemble_tlg_works_filepaths(
#     corpus_dir=conveted_tlg_dir
# )
# print("TLG works filepaths:", tlg_works_filepaths)

tlg_works_filepaths: list[str] = assemble_tlg_works_filepaths_for_author(
    corpus_dir=conveted_tlg_dir,
    author_id="0007",  # Plutarch
    work_id="001",  # ΘΗΣΕΥΣ ΚΑΙ ΡΩΜΥΛΟΣ
)
print("TLG work 001 for author 0007:", tlg_works_filepaths)

# Open files
for filepath in tlg_works_filepaths:
    print(f"Processing: {filepath}")
    with open(filepath, "r") as file:
        content = file.read()
    content = tlg_plaintext_cleanup(content)
    print(
        f"Cleaned content of {filepath}: {content[:100]}"
    )  # Print first 100 characters of cleaned content

    # Do further processing with cleaned content
    doc = nlp_grc.analyze(text=content)

    # Save doc as pickle
    with open(os.path.expanduser("~/Downloads/plutarch_cltk_doc.pickle"), "wb") as f:
        pickle.dump(doc, f)

    conllu_str: str = doc_to_conllu(doc)
    with open(os.path.expanduser("~/Downloads/plutarch_cltk_doc.conllu"), "w") as f:
        f.write(conllu_str)

    # `Requires `pyarrow` package: `pip install pyarrow`
    feature_table: pa.Table = doc_to_feature_table(doc)
    feather.write_feather(
        feature_table,
        os.path.expanduser("~/Downloads/plutarch_cltk_doc.feather"),
    )

    pacsv.write_csv(
        feature_table,
        os.path.expanduser("~/Downloads/plutarch_cltk_doc.csv"),
    )

    # For pyarrow table of features as a pandas table
    # Requires `pandas` package: `pip install pandas openpyxl`
    df: pd.DataFrame = feature_table.to_pandas()
    df.to_excel(os.path.expanduser("~/Downloads/plutarch_cltk_doc.xlsx"), index=False)

    if backend in ["openai", "ollama", "mistral"]:
        readers_guide: str = format_readers_guide(doc)
        with open(
            os.path.expanduser("~/Downloads/plutarch_readers_guide.md"), "w"
        ) as f:
            f.write(readers_guide)
