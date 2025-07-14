from dataclasses import dataclass, field
from typing import Optional

from cltk.core.data_types import Doc, Process
from cltk.core.exceptions import CLTKException
from cltk.genai.chatgpt import ChatGPT


@dataclass
class ChatGPTProcess(Process):
    """A Process type to capture everything that ChatGPT can do for a given language."""

    language: Optional[str] = None
    api_key: Optional[str] = None
    model: str = "gpt-4.1"
    temperature: float = 1.0
    description: str = "Process for ChatGPT for linguistic annotation."
    authorship_info: str = "ChatGPTProcess using OpenAI GPT models."
    chatgpt: Optional[ChatGPT] = field(init=False, default=None)

    def __post_init__(self):
        if self.language and self.api_key:
            self.chatgpt = ChatGPT(
                language=self.language,
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
            )
        else:
            self.chatgpt = None

    def run(self, input_doc: Doc) -> Doc:
        """Run ChatGPT inferencing and enrich the Doc with linguistic metadata."""
        if not self.chatgpt:
            raise ValueError("ChatGPTProcess requires language and api_key to be set.")
        # Use normalized_text if available, else raw
        input_text = (
            input_doc.normalized_text if input_doc.normalized_text else input_doc.raw
        )
        if not input_text:
            raise CLTKException(
                "Input document must have either normalized_text or raw text."
            )
        enriched_doc = self.chatgpt.generate_all(input_text=input_text)
        # Only overwrite fields if not None in input_doc
        if input_doc.language is not None:
            enriched_doc.language = input_doc.language
        if input_doc.normalized_text is not None:
            enriched_doc.normalized_text = input_doc.normalized_text
        if input_doc.raw is not None:
            enriched_doc.raw = input_doc.raw
        if input_doc.pipeline is not None:
            enriched_doc.pipeline = input_doc.pipeline
        return enriched_doc


@dataclass
class GreekChatGPTProcess(ChatGPTProcess):
    """ChatGPT processor for Ancient Greek."""

    language: Optional[str] = "grc"
    description: str = "Default process for ChatGPT for the Ancient Greek language."
    authorship_info: str = "GreekChatGPTProcess using OpenAI GPT models."


if __name__ == "__main__":
    import os

    from cltk.languages.example_texts import get_example_text
    from cltk.utils.utils import load_env_file

    load_env_file()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise CLTKException("Please set the OPENAI_API_KEY environment variable.")
    EXAMPLE_GRC = get_example_text("grc")
    doc = Doc(language="grc", raw=EXAMPLE_GRC)
    # process = ChatGPTProcess(
    #     language="grc", api_key=OPENAI_API_KEY, model="gpt-4.1", temperature=1.0
    # )
    process = GreekChatGPTProcess(
        language="grc", api_key=OPENAI_API_KEY, model="gpt-4.1", temperature=1.0
    )
    enriched_doc = process.run(doc)
    print(enriched_doc.words)
    print(enriched_doc.chatgpt)
