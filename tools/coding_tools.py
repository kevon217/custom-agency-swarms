import os
import sys
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


# Utility to get the full path for a given subdirectory and filename
def get_full_path(subdirectory, filename):
    agent_workdir = os.environ.get("AGENT_WORKING_DIR", ".")
    return os.path.join(agent_workdir, subdirectory, filename)


# Define Custom Coding-Related Tools:


class CheckInstalledPackages(BaseTool):
    """
    Checks and lists installed Python packages in the current environment.
    """

    chain_of_thought: str = Field(
        ...,
        description="Outline the reasoning behind checking the installed packages. Describe the packages expected to be used for the task and their purpose.",
    )

    def run(self):
        """
        Returns a list of installed packages in the current Python environment.
        """
        import pkg_resources

        installed_packages = [d.project_name for d in pkg_resources.working_set]
        return f"Chain of Thought: {self.chain_of_thought}\nInstalled Packages: {installed_packages}"


class GetWorkDirTree(BaseTool):
    """
    Reads and lists the directory tree of the working directory.
    """

    # directory_path: str = Field(..., description="The path of the working directory.") # not sure if i need

    def run(self):
        """
        Returns a formatted string representing the directory tree structure starting from the agent's working directory.
        """
        agent_workdir = os.environ.get("AGENT_WORKING_DIR", ".")
        tree_structure = []

        for root, dirs, files in os.walk(agent_workdir):
            level = root.replace(agent_workdir, "").count(os.sep)
            indent = " " * 4 * level
            tree_structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = " " * 4 * (level + 1)
            for file in files:
                tree_structure.append(f"{subindent}{file}")

        return "\n".join(tree_structure)


class ReadFile(BaseTool):
    """
    Read the contents of a specified file from a directory.
    """

    subdirectory: str = Field(
        ..., description="The subdirectory where the file is located."
    )
    file_name: str = Field(..., description="The name of the file to be read.")

    def run(self):
        """
        Reads the contents of the file specified by file_name in the subdirectory.
        Handles errors related to file not found or mismatches in the filename.
        Returns the contents of the file or an error message.
        """
        file_path = get_full_path(self.subdirectory, self.file_name)

        if not os.path.isfile(file_path):
            return f"Error: File '{self.file_name}' not found in '{self.subdirectory}'."

        try:
            with open(file_path, "r") as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error reading file: {e}"


class File(BaseTool):
    """
    Python file with an appropriate name, containing code that can be saved and executed locally at a later time.
    """

    subdirectory: str = Field(..., description="The subdirectory to write the file.")
    file_name: str = Field(
        ..., description="The name of the file including the extension"
    )
    body: str = Field(..., description="Correct contents of a file")

    def run(self):
        """
        Writes the contents to a file in the specified subdirectory.
        """
        file_path = get_full_path(self.subdirectory, self.file_name)

        # Create subdirectory if it does not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as f:
            f.write(self.body)

        return "File written to " + file_path


class ExecutePyFile(BaseTool):
    """
    Run existing python file from local disc.
    """

    subdirectory: str = Field(
        ..., description="The subdirectory where the .py file is located."
    )
    file_name: str = Field(..., description="The name of the .py file to be executed.")

    def run(self):
        """
        Executes a Python script at the given file path and captures its output and errors.
        """
        file_path = get_full_path(self.subdirectory, self.file_name)

        try:
            result = subprocess.run(
                [sys.executable, file_path],  # Use the same Python interpreter
                text=True,
                capture_output=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"An error occurred: {e.stderr}"


class Program(BaseTool):
    """
    Set of files that represent a complete and correct program.
    """

    chain_of_thought: str = Field(
        ...,
        description="Think step by step to determine the correct actions that are needed to implement the program.",
    )
    files: List[File] = Field(..., description="List of files")

    def run(self):
        outputs = []
        for file in self.files:
            outputs.append(file.run())

        return str(outputs)


# BE CAREFUL WITH THIS TOOL. IT CAN BE DANGEROUS IF USED INCORRECTLY.
# class ExecuteCommand(BaseTool):
#     """Run any command from the terminal. If there are too many logs, the outputs might be truncated."""

#     command: str = Field(..., description="The command to be executed.")

#     def run(self):
#         """Executes the given command and captures its output and errors."""
#         try:
#             # Splitting the command into a list of arguments
#             command_args = self.command.split()

#             # Executing the command
#             result = subprocess.run(
#                 command_args, text=True, capture_output=True, check=True
#             )
#             return result.stdout
#         except subprocess.CalledProcessError as e:
#             return f"An error occurred: {e.stderr}"
