import os
from dotenv import load_dotenv
import subprocess
from typing import Dict, List, Literal
from pydantic import Field, PrivateAttr
from pathlib import Path

from agency_swarm.tools import BaseTool
from agency_swarm import Agent, Agency, set_openai_key
from agency_swarm import Agency
from agency_swarm.tools import Retrieval, CodeInterpreter

from instructor import OpenAISchema

from instructions import (
    ceo_instructions,
    dev_instructions,
    analyst_instructions,
)
from ..DataGents.tools import (
    CheckInstalledPackages,
    GetWorkDirTree,
    ReadFile,
    File,
    ExecutePyFile,
    Program,
    SearchWeb,
)
from utils.workdir import init_agent_workdir


# Set Agent Working Directory

os.environ["AGENT_WORKING_DIR"] = init_agent_workdir(
    relative_path="DataGents/agent_workdir"
)

# Define Agent Roles

ceo = Agent(
    name="CEO_simple",
    description="Responsible for facilitating smooth and efficient communication between the user and specialized agents.",
    instructions=ceo_instructions,  # can be a file like ./instructions.md
    files_folder=None,
    tools=[],
)

dev = Agent(
    name="PYTHON_DEV",
    description="Responsible for creating and/or executing Python scripts to fulfill the user's request.",
    instructions=dev_instructions,
    files_folder=None,
    tools=[
        CheckInstalledPackages,
        GetWorkDirTree,
        ReadFile,
        File,
        ExecutePyFile,
        Program,
    ],
)

analyst = Agent(
    name="DATA_ANALYST",
    description="Responsible for analyzing data requests and outlining the steps needed to fulfill the request.",
    instructions=analyst_instructions,
    files_folder=None,
    tools=[SearchWeb],
)

# Add Shared Instructions
fp_shared_instructions = os.getcwd() + "DataGents\\instructions\\manifesto.md"


# 4. Define Agency Communication Flows
# agency = Agency(
#     [
#         ceo,
#         [ceo, analyst],
#         [analyst, dev],
#         [ceo, analyst, dev],
#         [analyst, ceo]
#     ],
#     shared_instructions=fp_shared_instructions,
# )

agency = Agency(
    [
        ceo,
        [ceo, dev],
    ],
    shared_instructions=fp_shared_instructions,
)


# 5. Run Demo
agency.demo_gradio(height=900)
