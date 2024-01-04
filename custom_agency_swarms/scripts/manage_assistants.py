"""
Example usage:

- python manage_assistants.py list
- python manage_assistants.py list_brief
- python manage_assistants.py delete --id asst_abc123
- python manage_assistants.py delete_multiple --ids asst_abc123 asst_def456
- python manage_assistants.py modify --id asst_abc123 --params '{"name": "New Name", "description": "New Description"}'
- python manage_assistants.py list_files --id asst_abc123
- python manage_assistants.py create --name "Math Tutor" --instructions "You are a personal math tutor..." --model "gpt-4" --tools '[{"type": "code_interpreter"}]'
- python manage_assistants.py create_file --assistant_id "asst_abc123" --file_id "file-abc123"
- python manage_assistants.py retrieve --id asst_abc123
- python manage_assistants.py retrieve_file --assistant_id "asst_abc123" --file_id "file-abc123"
- python manage_assistants.py retrieve_by_name --name "Math Tutor"
"""

import argparse
import logging
import json

from agency_swarm.util.oai import get_openai_client
from custom_agency_swarms.utils.assistant_helper import (
    list_assistants,
    inspect_assistants,
    list_assistant_files,
    modify_assistant,
    delete_assistant_file,
    delete_assistant,
    delete_assistants,
    create_assistant,
    create_assistant_file,
    retrieve_assistant,
    retrieve_assistant_file,
    retrieve_assistant_by_name,
)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage OpenAI Assistants")
    parser.add_argument(
        "action",
        choices=[
            "list",
            "list_brief",
            "delete",
            "delete_multiple",
            "modify",
            "list_file_ids",
            "create",
            "create_file",
            "retrieve",
            "retrieve_file",
            "retrieve_by_name",
        ],
        help="Action to perform",
    )
    parser.add_argument("--id", help="Assistant ID for specific actions")
    parser.add_argument(
        "--ids", nargs="*", help="List of Assistant IDs for batch delete"
    )
    parser.add_argument(
        "--params", help="JSON string with parameters for modify action"
    )
    parser.add_argument("--name", help="Name of the assistant")
    parser.add_argument("--instructions", help="Instructions for the assistant")
    parser.add_argument("--model", help="Model of the assistant")
    parser.add_argument("--tools", help="Tools for the assistant")
    parser.add_argument("--file_id", help="File ID for creating or retrieving a file")
    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()
    client = get_openai_client()  # Initialize the client

    # Existing actions ...

    if args.action == "create":
        created_assistant = create_assistant(
            client, args.name, args.instructions, args.model, json.loads(args.tools)
        )
        print(json.dumps(created_assistant.model_dump(), indent=4))

    elif args.action == "create_file":
        created_file = create_assistant_file(client, args.id, args.file_id)
        print(json.dumps(created_file.model_dump(), indent=4))

    elif args.action == "retrieve":
        retrieved_assistant = retrieve_assistant(client, args.id)
        print(json.dumps(retrieved_assistant.model_dump(), indent=4))

    elif args.action == "retrieve_file":
        retrieved_file = retrieve_assistant_file(client, args.id, args.file_id)
        print(json.dumps(retrieved_file.model_dump(), indent=4))

    elif args.action == "retrieve_by_name":
        retrieved_assistant = retrieve_assistant_by_name(client, args.name)
        print(json.dumps(retrieved_assistant.model_dump(), indent=4))

    else:
        logging.error("Invalid arguments. Please check the usage.")


if __name__ == "__main__":
    main()
