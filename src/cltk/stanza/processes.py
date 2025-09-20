"""Processes backed by Stanford Stanza (optional extra).

This module provides a single StanzaAnalyzeProcess that runs a stanza.Pipeline
and fills a CLTK Doc with sentence boundaries and token-level annotations
(lemma, UPOS, FEATS, HEAD, DEPREL).

Requires optional extra: pip install "cltk[stanza]"
"""

from typing import Optional

from stanza import DownloadMethod

from cltk.core.cltk_logger import bind_context
from cltk.core.data_types import Doc, Process, Word
from cltk.morphosyntax.ud_deprels import UDDeprelTag, get_ud_deprel_tag
from cltk.morphosyntax.ud_features import UDFeatureTagSet, convert_pos_features_to_ud
from cltk.morphosyntax.ud_pos import UDPartOfSpeechTag

_GLOTTO_TO_STANZA_LANG = {
    "chur1257": "Old_Church_Slavonic",
    "copt1239": "Coptic",
    "oldf1239": "Old_French",
    "anci1242": "Ancient_Greek",
    "goth1244": "Gothic",
    "lati1261": "Latin",
    "lite1248": "Classical_Chinese",
    "olde1238": "Old_English",
    "otto1234": "Ottoman_Turkish",
    "clas1256": "Classical_Armenian",
    "oldr1238": "Old_East_Slavic",  # treebank names changed from Old Russian to Old East Slavic in 2.8
}


class StanzaAnalyzeProcess(Process):
    """Run Stanza and populate a Doc with UD annotations.

    Notes:
      - If Stanza is not installed, raises an ImportError with guidance to
        install the optional extra.
      - Uses Stanza defaults; language package must be available locally or it
        will trigger Stanza's download mechanism externally.

    """

    def run(self, input_doc: Doc) -> Doc:
        output_doc = Doc(**input_doc.model_dump())
        log = bind_context(
            glottolog_id=getattr(self, "glottolog_id", None), model="stanza"
        )

        if not output_doc.normalized_text:
            raise ValueError("Doc must have `normalized_text` to run Stanza.")

        # Optional dependency guard
        try:
            import stanza
        except Exception as e:  # pragma: no cover - only when stanza missing
            raise ImportError(
                "Stanza not installed. Install with: pip install 'cltk[stanza]'"
            ) from e

        lang = _GLOTTO_TO_STANZA_LANG.get(
            getattr(self, "glottolog_id", None) or output_doc.language.glottolog_id
        )
        if not lang:
            raise ValueError(
                f"No Stanza language mapping for glottolog_id='{self.glottolog_id}'."
            )

        # Build Stanza pipeline; let it handle sentence splitting and tagging
        nlp = stanza.Pipeline(
            lang=lang,
            processors="tokenize,pos,lemma,depparse",
            tokenize_no_ssplit=False,
            download_method=DownloadMethod.REUSE_RESOURCES,
        )
        sdoc = nlp(output_doc.normalized_text)

        words: list[Word] = []
        sent_bounds: list[tuple[int, int]] = []
        token_counter = 0
        for s_idx, sent in enumerate(getattr(sdoc, "sentences", []) or []):
            # Sentence boundary from token char offsets when available
            s_tokens = getattr(sent, "tokens", []) or []
            s_start = None
            s_end = None
            for t in s_tokens:
                sc = getattr(t, "start_char", None)
                ec = getattr(t, "end_char", None)
                if isinstance(sc, int):
                    s_start = sc if s_start is None else min(s_start, sc)
                if isinstance(ec, int):
                    s_end = ec if s_end is None else max(s_end, ec)
            if s_start is not None and s_end is not None:
                sent_bounds.append((s_start, s_end))

            # Stanza words for dependency info (head/deprel) live under sent.words
            for w in getattr(sent, "words", []) or []:
                form = getattr(w, "text", None)
                lemma = getattr(w, "lemma", None)
                upos_s = getattr(w, "upos", None)
                feats_s = getattr(w, "feats", None)
                head_i = getattr(w, "head", None)
                deprel_s = getattr(w, "deprel", None)

                # UPOS
                upos_obj: Optional[UDPartOfSpeechTag] = None
                if isinstance(upos_s, str) and upos_s:
                    try:
                        upos_obj = UDPartOfSpeechTag(tag=upos_s)
                    except Exception:
                        upos_obj = None

                # FEATS
                feats_obj: Optional[UDFeatureTagSet] = None
                if isinstance(feats_s, str) and feats_s and feats_s != "_":
                    try:
                        feats_obj = convert_pos_features_to_ud(feats_raw=feats_s)
                    except Exception:
                        feats_obj = None

                # DEPREL
                dep_obj: Optional[UDDeprelTag] = None
                if isinstance(deprel_s, str) and deprel_s:
                    main, subtype = (deprel_s.split(":", 1) + [None])[:2]
                    try:
                        if isinstance(main, str):
                            dep_obj = get_ud_deprel_tag(main, subtype=subtype)
                    except Exception:
                        dep_obj = None

                # HEAD (convert UD 1-based to 0-based)
                gov: Optional[int] = None
                try:
                    if isinstance(head_i, int):
                        gov = None if head_i == 0 else head_i - 1
                except Exception:
                    gov = None

                # Character offsets at word-level (best effort from token grouping)
                # Stanza exposes start_char for tokens; words may not carry it directly
                start_char = getattr(w, "start_char", None)
                end_char = getattr(w, "end_char", None)

                word = Word(
                    string=form,
                    index_token=token_counter,
                    index_sentence=s_idx,
                    lemma=lemma,
                    upos=upos_obj,
                    features=feats_obj,
                    dependency_relation=dep_obj,
                    governor=gov,
                )
                if isinstance(start_char, int) and isinstance(end_char, int):
                    word.index_char_start = start_char
                    word.index_char_stop = end_char

                words.append(word)
                token_counter += 1

        output_doc.words = words
        if sent_bounds:
            output_doc.sentence_boundaries = sent_bounds
        log.info(
            "Stanza annotated %d sentences and %d tokens", len(sent_bounds), len(words)
        )
        return output_doc
