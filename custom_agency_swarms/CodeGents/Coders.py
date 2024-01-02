import os
from agency_swarm import Agent, Agency
from instructions import (
    ceo_instructions,
    dev_instructions,
    analyst_instructions,
)
from custom_agency_swarms.tools import (
    CheckInstalledPackages,
    GetWorkDirTree,
    ReadFile,
    File,
    ExecutePyFile,
    Program,
)
from custom_agency_swarms.utils.workdir import init_agent_workdir


# Set Agent Working Directory

os.environ["AGENT_WORKING_DIR"] = init_agent_workdir(
    relative_path="custom_agency_swarms/CodeGents/agent_workdir"
)

# Define Agent Roles

ceo = Agent(
    name="CodeGents_CEO",
    description="Responsible for facilitating smooth and efficient communication between the user and specialized agents.",
    instructions=ceo_instructions,  # can be a file like ./instructions.md
    files_folder=None,
    tools=[],
)

dev = Agent(
    name="CodeGents_PYDEV",
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
    name="CodeGents_ANALYST",
    description="Responsible for analyzing data requests and outlining the steps needed to fulfill the request.",
    instructions=analyst_instructions,
    files_folder=None,
    tools=[],
)

# Add Shared Instructions (Manifesto)
fp_shared_instructions = (
    os.getcwd() + "\\custom_agency_swarms\\CodeGents\\instructions\\manifesto.md"
)
with open(fp_shared_instructions, "r") as file:
    shared_instructions = file.read()

# 4. Define Agency Communication Flows
agency = Agency(
    [
        ceo,
        [ceo, analyst],
        [analyst, dev],  # Analyst can directly instruct and collaborate with Developer
        [dev, analyst],  # Developer can seek clarification or verify steps with Analyst
        [
            ceo,
            dev,
        ],  # CEO can still communicate directly with Developer for high-level task management
    ],
    shared_instructions=shared_instructions,
)

# 5. Run Demo
agency.demo_gradio(height=900)
