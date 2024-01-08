import os
from agency_swarm import Agent, Agency
from instructions import (
    ceo_instructions,
    req_analyst_instructions,
    sys_designer_instructions,
    py_dev_instructions,
    code_reviewer_instructions,
    sys_architect_instructions,
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

req_analyst = Agent(
    name="CodeGents_REQ-ANALYST",
    description="Analyzes and articulates project requirements, ensuring clarity and feasibility.",
    instructions=req_analyst_instructions,
    files_folder=None,
    tools=[],
)

sys_designer = Agent(
    name="CodeGents_SYS-DESIGNER",
    description="Designs the system's structure, integrating SOLID principles and best practices.",
    instructions=sys_designer_instructions,
    files_folder=None,
    tools=[],
)

py_dev = Agent(
    name="CodeGents_PY-DEV",
    description="Develops Python scripts, focusing on functionality, efficiency, and adherence to design specifications.",
    instructions=py_dev_instructions,
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

code_reviewer = Agent(
    name="CodeGents_CODE-REVIEWER",
    description="Reviews code for quality, consistency with design patterns, and best practice compliance.",
    instructions=code_reviewer_instructions,
    files_folder=None,
    tools=[GetWorkDirTree, CheckInstalledPackages, ReadFile],
)

sys_architect = Agent(
    name="CodeGents_SYS-ARCHITECT",
    description="Oversees system architecture, guiding structural decisions and ensuring alignment with design and development.",
    instructions=sys_architect_instructions,
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
        [ceo, req_analyst],
        [req_analyst, sys_designer],
        [sys_designer, sys_architect],
        [sys_designer, py_dev],
        [py_dev, sys_designer],
        [py_dev, code_reviewer],
        [code_reviewer, ceo],
        [sys_architect, sys_designer],
        [sys_architect, ceo],
    ],
    shared_instructions=shared_instructions,
)

# 5. Run Demo
agency.demo_gradio(height=900)
