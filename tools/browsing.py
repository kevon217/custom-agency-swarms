import os
from dotenv import load_dotenv
import subprocess
from typing import Dict, List, Literal
from pydantic import Field, PrivateAttr
from duckduckgo_search import DDGS

from agency_swarm.tools import BaseTool
from agency_swarm import set_openai_key
from agency_swarm.util import get_openai_client

from instructor import OpenAISchema


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
set_openai_key(OPENAI_API_KEY)
client = get_openai_client()


class SearchWeb(BaseTool):
    """Search the web with a search phrase and return the results."""

    phrase: str = Field(
        ...,
        description="The search phrase you want to use. Optimize the search phrase for an internet search engine.",
    )

    # This code will be executed if the agent calls this tool
    def run(self):
        with DDGS() as ddgs:
            return str([r for r in ddgs.text(self.phrase, max_results=3)])
