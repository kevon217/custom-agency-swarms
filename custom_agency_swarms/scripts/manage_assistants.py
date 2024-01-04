"""
Example usage:

- List all assistants: python manage_assistants.py list
- List brief details of assistants: python manage_assistants.py list_brief
- Delete a specific assistant: python manage_assistants.py delete --id asst_abc123
- Delete multiple assistants: python manage_assistants.py delete_multiple --ids asst_abc123 asst_def456
- Modify an assistant: python manage_assistants.py modify --id asst_abc123 --params '{"name": "New Name", "description": "New Description"}'
- List files of an assistant: python manage_assistants.py list_files --id asst_abc123
- Create an assistant: python manage_assistants.py create --name "Math Tutor" --instructions "You are a personal math tutor..." --model "gpt-4" --tools '[{"type": "code_interpreter"}]'
- Create a file for an assistant: python manage_assistants.py create_file --id "asst_abc123" --file_id "file-abc123"
- Retrieve an assistant: python manage_assistants.py retrieve --id asst_abc123
- Retrieve a file of an assistant: python manage_assistants.py retrieve_file --id "asst_abc123" --file_id "file-abc123"
- Retrieve an assistant by name: python manage_assistants.py retrieve_by_name --name "Math Tutor"
- Delete assistants within a specified date range: python manage_assistants.py delete_range --start_date "2024-01-04" --end_date "2024-01-05"
"""

import argparse
import logging
import json

from agency_swarm.util.oai import get_openai_client
from custom_agency_swarms.utils.helper import parse_date, filter_fobjs_by_date_range
from custom_agency_swarms.utils.assistant_helper import (
    list_assistants,
    inspect_assistants,
    list_assistant_files,
    update_assistant,
    delete_assistant,
    delete_assistants,
    delete_assistant_file,
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
            "inspect",
            "create",
            "create_file",
            "retrieve",
            "retrieve_by_name",
            "list_files",
            "retrieve_file",
            "delete_file",
            "update_assistant",
            "delete",
            "delete_mult",
            "delete_range",
        ],
        help="Action to perform",
    )
    parser.add_argument("--id", help="Assistant ID for specific actions")
    parser.add_argument(
        "--ids", nargs="*", help="List of Assistant IDs for batch delete"
    )
    parser.add_argument("--name", help="Name of the assistant")
    parser.add_argument(
        "--keys", nargs="*", help="List of keys to inspect in assistants"
    )
    parser.add_argument("--instructions", help="Instructions for the assistant")
    parser.add_argument("--model", help="Model of the assistant")
    parser.add_argument("--tools", help="Tools for the assistant")
    parser.add_argument("--file_id", help="File ID for creating or retrieving a file")
    parser.add_argument(
        "--params", help="JSON string with parameters for update action"
    )
    parser.add_argument(
        "--start_date", help="Start date for delete_range action (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end_date", help="End date for delete_range action (YYYY-MM-DD)"
    )
    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()
    client = get_openai_client()  # Initialize the client

    if args.action == "list":
        assistants = list_assistants(client)
        for assistant in assistants:
            print(json.dumps(assistant.model_dump(), indent=4))
        return assistants

    elif args.action == "inspect":
        assistants = list_assistants(client)
        keys = args.keys if args.keys else None  # Use provided keys if available
        assistants_info = (
            inspect_assistants(assistants)(keys)
            if keys
            else inspect_assistants(assistants)()
        )
        print(json.dumps(assistants_info, indent=4))

    elif args.action == "create":
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

    elif args.action == "retrieve_by_name":
        retrieved_assistant = retrieve_assistant_by_name(client, args.name)
        print(json.dumps(retrieved_assistant.model_dump(), indent=4))

    elif args.action == "list_files":
        if args.id:
            files = list_assistant_files(client, args.id)
            print(json.dumps(files, indent=4, default=lambda o: o.__dict__))
        else:
            logging.error("Assistant ID is required for list_files action.")

    elif args.action == "retrieve_file":
        retrieved_file = retrieve_assistant_file(client, args.id, args.file_id)
        print(json.dumps(retrieved_file.model_dump(), indent=4))

    elif args.action == "delete_file":
        if args.id and args.file_id:
            response = delete_assistant_file(client, args.id, args.file_id)
            print(json.dumps(response.__dict__, indent=4))
        else:
            logging.error(
                "Assistant ID and file ID are required for delete_file action."
            )

    elif args.action == "update_assistant":
        if args.id and args.params:
            params = json.loads(args.params)
            updated_assistant = update_assistant(client, args.id, **params)
            print(json.dumps(updated_assistant.__dict__, indent=4))
        else:
            logging.error(
                "Assistant ID and params are required for update_assistant action."
            )

    elif args.action == "delete":
        if args.id:
            response = delete_assistant(client, args.id)
            print(json.dumps(response.__dict__, indent=4))
        else:
            logging.error("Assistant ID is required for delete action.")

    elif args.action == "delete_mult":
        if args.ids:
            delete_results = delete_assistants(client)(args.ids)
            print(json.dumps(delete_results, indent=4))
        else:
            logging.error("Assistant IDs are required for delete_multiple action.")

    elif args.action == "delete_range":
        start_date = parse_date(args.start_date) if args.start_date else None
        end_date = parse_date(args.end_date) if args.end_date else None

        if not start_date or not end_date:
            logging.error(
                "Both start_date and end_date are required for delete_range action."
            )
            return

        assistant_objs = list_assistants(client)
        assistants_to_delete = filter_fobjs_by_date_range(
            assistant_objs, start_date, end_date
        )
        assistant_ids_to_delete = [assistant.id for assistant in assistants_to_delete]

        delete_function = delete_assistants(client)
        delete_results = delete_function(assistant_ids_to_delete)
        print(json.dumps(delete_results, indent=4))
    else:
        logging.error("Invalid arguments. Please check the usage.")


if __name__ == "__main__":
    main()
