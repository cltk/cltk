import os
import unittest

import pytest

from cltk import NLP
from cltk.core.data_types import Doc
from cltk.genai.chatgpt import ChatGPTV1
from cltk.languages.example_texts import get_example_text
from cltk.languages.pipelines import AncientGreekChatGPTPipeline


def test_chatgpt_init():
    chatgpt = ChatGPTV1(language_code="lat", api_key="sk-test")
    assert chatgpt.language.name == "Latin"
    assert chatgpt.api_key == "sk-test"


def test_prompt_construction():
    chatgpt = ChatGPTV1(language_code="lat", api_key="sk-test")
    prompt = chatgpt.generate_pos(
        "Gallia est omnis divisa in partes tres.", print_raw_response=False
    )
    assert isinstance(prompt, Doc)


def test_fallback_word_info():
    chatgpt = ChatGPTV1(language_code="lat", api_key="sk-test")
    # Simulate a malformed response
    result = chatgpt._parse_word_info_from_chatgpt_response(
        "", print_raw_response=False
    )
    assert isinstance(result, dict)


def test_metadata_aggregation():
    chatgpt = ChatGPTV1(language_code="lat", api_key="sk-test")
    doc = chatgpt._post_process_pos_response(
        "Gallia\tGallia\tGallia\tO\tNOUN\tNOUN\tNOUN",
        "Gallia",
        chatgpt_response_obj=None,
        print_raw_response=False,
    )
    assert hasattr(doc, "chatgpt")


def test_missing_api_key():
    os.environ.pop("OPENAI_API_KEY", None)
    with pytest.raises(Exception):
        ChatGPTV1(language_code="lat", api_key=None)  # type: ignore intentional bad parameter


class TestChatGPTNLP(unittest.TestCase):
    def test_greek_chatgpt_pipeline(self):
        example_text = get_example_text("grc")
        pipeline = AncientGreekChatGPTPipeline()
        nlp = NLP(language_code="grc", custom_pipeline=pipeline, suppress_banner=True)
        doc = nlp.analyze(example_text)
        # Basic assertions
        self.assertIsNotNone(doc)
        self.assertTrue(hasattr(doc, "words"))
        self.assertIsInstance(doc.words, list)
        self.assertIsNotNone(doc.words)
        if doc.words is not None:
            self.assertGreater(len(doc.words), 0)
        self.assertTrue(hasattr(doc, "chatgpt"))
        self.assertIsInstance(doc.chatgpt, dict)
        # Print for manual inspection (optional)
        print(doc)
        print("Words:", [w.string for w in doc.words] if doc.words is not None else [])
        print("ChatGPT metadata:", doc.chatgpt)
