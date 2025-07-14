import os
import unittest
import pytest
from cltk.genai.chatgpt import ChatGPT
from cltk.core.data_types import Doc
from cltk import NLP
from cltk.languages.example_texts import get_example_text
from cltk.languages.pipelines import GreekChatGPTPipeline

def test_chatgpt_init():
    chatgpt = ChatGPT(language="lat", api_key="sk-test")
    assert chatgpt.language.name == "Latin"
    assert chatgpt.api_key == "sk-test"

def test_prompt_construction():
    chatgpt = ChatGPT(language="lat", api_key="sk-test")
    prompt = chatgpt.generate_pos("Gallia est omnis divisa in partes tres.", print_raw_response=False)
    assert isinstance(prompt, Doc)

def test_fallback_word_info():
    chatgpt = ChatGPT(language="lat", api_key="sk-test")
    # Simulate a malformed response
    result = chatgpt._get_word_info("", print_raw_response=False)
    assert isinstance(result, dict)

def test_metadata_aggregation():
    chatgpt = ChatGPT(language="lat", api_key="sk-test")
    doc = chatgpt._post_process_response("Gallia\tGallia\tGallia\tO\tNOUN\tNOUN\tNOUN", "Gallia", response_obj=None, print_raw_response=False)
    assert hasattr(doc, "chatgpt")

def test_missing_api_key():
    os.environ.pop("OPENAI_API_KEY", None)
    with pytest.raises(Exception):
        ChatGPT(language="lat", api_key=None) # type: ignore intentional bad parameter

class TestChatGPTNLP(unittest.TestCase):
    def test_greek_chatgpt_pipeline(self):
        example_text = get_example_text("grc")
        pipeline = GreekChatGPTPipeline()
        nlp = NLP(language="grc", custom_pipeline=pipeline, suppress_banner=True)
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
