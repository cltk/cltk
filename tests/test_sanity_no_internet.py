"""A quick sanity check for testing library without downloads or
 a network connection."""

import unittest
from typing import List

from boltons.strutils import split_punct_ws

from cltk import NLP
from cltk.core.data_types import Doc, Pipeline, Process, Word
from cltk.languages.example_texts import get_example_text
from cltk.stops.processes import StopsProcess


class TestNoInternet(unittest.TestCase):
    """Quick test."""

    def test_nlp_latin_stops(self):
        lang = "lat"  # type: str
        cltk_nlp = NLP(language=lang)  # type: NLP
        self.assertIsInstance(cltk_nlp, NLP)
        lat_pipeline = cltk_nlp.pipeline  # type: Pipeline
        pipeline_just_stops = [
            proc for proc in lat_pipeline.processes if proc.__name__ == "StopsProcess"
        ]  # type: List[Process]
        self.assertEqual(len(pipeline_just_stops), 1)
        stops_class = pipeline_just_stops[0]  # type: StopsProcess
        self.assertIs(stops_class, StopsProcess)
        words = [Word(string=token) for token in split_punct_ws(get_example_text(lang))]
        doc = Doc(words=words)
        stops_obj = stops_class(language=lang)
        output_doc = stops_obj.run(input_doc=doc)
        is_stops = [w.stop for w in output_doc.words]  # type: List[bool]
        self.assertEqual(len(words), len(is_stops))
        self.assertIsInstance(is_stops[0], bool)


if __name__ == "__main__":
    unittest.main()
