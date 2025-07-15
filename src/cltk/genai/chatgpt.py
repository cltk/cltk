"""Call ChatGPT."""

import os

# from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from cltk.utils.utils import load_env_file

load_env_file()
# load_dotenv()  # loads .env into os.environ

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    response = client.responses.create(
        model="gpt-4.1", input="Write a one-sentence bedtime story about a unicorn."
    )
except OpenAIError as e:
    raise OpenAIError(f"An error from OpenAI occurred: {e}")

print(response.output_text)
