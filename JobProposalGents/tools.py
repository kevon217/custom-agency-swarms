import os
from dotenv import load_dotenv
import subprocess
from typing import Dict, List, Literal
from pydantic import Field, PrivateAttr

from agency_swarm.tools import BaseTool
from agency_swarm import set_openai_key, get_openai_client

from instructor import OpenAISchema


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
set_openai_key(OPENAI_API_KEY)
client = get_openai_client()


# 2. Define Your Custom Tool:
class ExecutePyFile(BaseTool):
    """Run existing python file from local disc."""

    file_name: str = Field(..., description="The path to the .py file to be executed.")

    def run(self):
        """Executes a Python script at the given file path and captures its output and errors."""
        try:
            result = subprocess.run(
                ["python3", self.file_name], text=True, capture_output=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e.stderr}"


class File(BaseTool):
    """
    Python file with an appropriate name, containing code that can be saved and executed locally at a later time. This environment has access to all standard Python packages and the internet.
    """

    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the correct actions that are needed to be taken in order to complete the task.",
    )
    file_name: str = Field(
        ..., description="The name of the file including the extension"
    )
    body: str = Field(..., description="Correct contents of a file")

    def run(self):
        with open(self.file_name, "w") as f:
            f.write(self.body)

        return "File written to " + self.file_name


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
