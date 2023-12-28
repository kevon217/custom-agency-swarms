import os
from dotenv import load_dotenv
import subprocess
from typing import Dict, List, Literal
from pydantic import Field, PrivateAttr

from agency_swarm.tools import BaseTool
from agency_swarm import set_openai_key
from agency_swarm.util import get_openai_client

from instructor import OpenAISchema


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
set_openai_key(OPENAI_API_KEY)
client = get_openai_client()


class ExtractJobDetails(BaseTool):
    """Extract key job details from a job posting."""

    title: str = Field(..., description="The title of the job")
    description: str = Field(..., description="A description of the job")
    challenges: str = Field(..., description="The challenges associated with the job")
    required_skills: List[str] = Field(
        ..., description="List of required skills for the job"
    )
    expertise_areas: List[str] = Field(
        ..., description="List of expertise areas relevant to the job"
    )
    expected_output: str = Field(..., description="The expected output of the job")

    def run(self):
        # Here, implement the logic to format the proposal prompt
        job_details = self.model_dump_json()
        return job_details


class GenerateProposal(BaseTool):
    """Generate a proposal for a project based on project details. Remember that user does not have access to the output of this function. You must send it back to him after execution."""

    chain_of_thought: str = Field(
        ...,
        description="Step by step thought process for generating the job proposal draft.",
    )
    job_details: str = Field(
        ..., description="The job posting details to generate a proposal for."
    )

    def run(self):
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional proposal drafting assistant. Do not include any actual technologies or technical details into proposal until specified in the project brief. Be short.",
                },
                {
                    "role": "user",
                    "content": "Please draft a proposal for the following job posting: "
                    + self.job_details,
                },
            ],
        )

        return str(completion.choices[0].message.content)
