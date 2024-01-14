# workdir.py
import os
import shutil
import logging
from pathlib import Path
import platform

# Initialize logging
logging.basicConfig(level=logging.INFO)


def create_init_file(path: Path):
    """
    Creates an __init__.py file in the specified directory.
    """
    init_file = path / "__init__.py"
    init_file.touch()  # Creates the file if it doesn't exist
    logging.info(f"Created __init__.py at: {init_file}")


def create_readme(path: Path):
    """
    Creates a README.md file in the specified directory.
    """
    readme_file = path / "README.md"
    readme_file.touch()  # Creates the file if it doesn't exist
    logging.info(f"Created README.md at: {readme_file}")


def create_requirements_txt(path: Path):
    """
    Creates a requirements.txt file in the specified directory.
    """
    requirements_file = path / "requirements.txt"
    requirements_file.touch()  # Creates the file if it doesn't exist
    logging.info(f"Created requirements.txt at: {requirements_file}")


def create_env_file(path: Path, source_env_path: Path):
    """
    Creates a .env file in the specified directory and copies the OPENAI_API_KEY from the source .env file.
    """
    env_file = path / ".env"
    try:
        with open(source_env_path, "r") as src, open(env_file, "w") as dst:
            lines = src.readlines()
            for line in lines:
                if line.startswith("OPENAI_API_KEY"):
                    dst.write(line)
                    break
        logging.info(f"Created .env file at: {env_file}")
    except FileNotFoundError:
        logging.error(f"Source .env file not found at: {source_env_path}")
    except Exception as e:
        logging.error(f"Error creating .env file: {e}")


def create_config_yaml(path: Path):
    """
    Creates a config.yaml file in the specified directory.
    """
    config_file = path / "config.yaml"
    config_file.touch()  # Creates the file if it doesn't exist
    logging.info(f"Created config.yaml at: {config_file}")


def create_main_py(path: Path):
    """
    Creates a main.py file in the specified directory.
    """
    main_file = path / "main.py"
    main_file.touch()  # Creates the file if it doesn't exist
    logging.info(f"Created main.py at: {main_file}")


def create_agent_workdir_structure(base_dir: Path, source_env_path: Path):
    """
    Creates the agent's working directory structure.
    """
    subdirectories = [
        "data/external",
        "data/interim",
        "data/processed",
        "data/raw",
        "notebooks",
        "reports",
        "reports/figures",
        "src",
        "src/features",
        "src/models",
        "src/visualization",
        "tests",
        "utils",
    ]

    for subdir in subdirectories:
        dir_to_create = base_dir / subdir
        dir_to_create.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created subdirectory: {dir_to_create}")

        # Create __init__.py in each subdirectory
        create_init_file(dir_to_create)

    # Create misc files as root of the agent's working directory
    create_main_py(base_dir)
    create_init_file(base_dir)
    create_config_yaml(base_dir)
    create_readme(base_dir)
    create_requirements_txt(base_dir)
    create_env_file(base_dir, source_env_path)


def init_agent_workdir(relative_path: str) -> str:
    """
    Initializes the agent's working directory.
    """
    # Determine current OS
    current_os = platform.system()
    # Use the current working directory's .env file
    source_env_path = Path.cwd() / ".env"

    # Construct the Path object
    if current_os == "Windows" and not relative_path.startswith("\\\\"):
        # For Windows, ensure correct format
        agent_workdir = Path.cwd() / Path(relative_path.replace("/", "\\"))
    else:
        # For Unix-like systems
        agent_workdir = Path.cwd() / relative_path

    logging.info(f"Initializing agent's working directory: {agent_workdir}")

    # Check if the directory exists, create if not
    if not agent_workdir.exists():
        logging.info(
            "Agent's working directory not found. Creating directory structure."
        )
        create_agent_workdir_structure(agent_workdir, source_env_path=source_env_path)
    else:
        logging.info("Agent's working directory already exists.")

    return str(agent_workdir.resolve())


# Example usage
if __name__ == "__main__":
    workdir = init_agent_workdir("agent_workdir")
    print(f"Agent Working Directory Initialized: {workdir}")
