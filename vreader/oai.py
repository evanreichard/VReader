from dataclasses import dataclass
from textwrap import indent
from typing import Any, List
import json
import openai

INITIAL_PROMPT_TEMPLATE = """
The following is a video transcription. Write a fully comprehensive article in markdown appropriately utilizing subsections. Be sure to only use the following transcription to write the article:

{context}
"""

INITIAL_PROMPT_TEMPLATE_OLD = """
The following is a video transcription. Write a comprehensive article in markdown utilizing the following content:

{context}
"""

@dataclass
class ChatCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: List[dict]
    usage: dict


class OpenAIConnector:
    def __init__(self, api_key: str | None):
        if api_key is None:
            raise RuntimeError("OPENAI_API_KEY Required")

        # self.model = "gpt-3.5-turbo-16k"
        self.model = "gpt-3.5-turbo-1106"
        self.word_cap = 1000
        openai.api_key = api_key


    def query(self, context: str) -> Any:
        # Create Initial Prompt
        prompt = INITIAL_PROMPT_TEMPLATE.format(context = context)
        messages = [{"role": "user", "content": prompt}]

        print("[OpenAIConnector] Running OAI Query")

        # Article Call
        response: ChatCompletion = openai.ChatCompletion.create( # type: ignore
          model=self.model,
          messages=messages
        )

        # Markdown Data
        content = response.choices[0]["message"]["content"]
        title = self.get_title(content)

        print("[OpenAIConnector] Completed OAI Query:\n", indent(json.dumps({ "usage": response.usage }, indent=2), ' ' * 2))

        # Return Response
        return { "title": title, "content": content }

    def get_title(self, markdown: str):
        lines = markdown.split('\n')
        for line in lines:
            if line.startswith("# "):
                return line.strip("# ").strip()
        return None
