"""
Example usage:

- List all files: python manage_files.py list_files
- Parse and display specific fields from files: python manage_files.py parse_file_objs --fields id,filename
- Retrieve details of a specific file: python manage_files.py retrieve --id file-abc123
- Delete a specific file: python manage_files.py delete --id file-abc123
- Retrieve content of a specific file: python manage_files.py retrieve_content --id file-abc123
- Delete files within a specified date range: python manage_files.py delete_range --start_date "2024-01-04" --end_date "2024-01-05"
"""

import argparse
import logging
import json

from agency_swarm.util.oai import get_openai_client
from custom_agency_swarms.utils.helper import parse_date, filter_fobjs_by_date_range
from custom_agency_swarms.utils.file_helper import (
    list_file_objs,
    parse_file_objs,
    retrieve_file,
    retrieve_file_content,
    delete_file,
    delete_files_batch,
)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage OpenAI Uploaded Files")
    parser.add_argument(
        "action",
        choices=[
            "list_files",
            "parse_file_objs",
            "retrieve",
            "delete",
            "retrieve_content",
            "delete_range",
        ],
        help="Action to perform",
    )
    parser.add_argument("--id", help="File ID for specific actions")
    parser.add_argument(
        "--fields",
        help="Comma-separated list of fields to display (for parse_file_objs)",
    )
    parser.add_argument(
        "--start_date",
        help="Start date for deletion range (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)",
    )
    parser.add_argument(
        "--end_date",
        help="End date for deletion range (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)",
    )

    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()
    client = get_openai_client()  # Initialize the client

    if args.action == "list_files":
        file_objs = list_file_objs(client)
        print(json.dumps(file_objs, indent=4, default=lambda o: o.__dict__))

    elif args.action == "parse_file_objs":
        fields = args.fields.split(",") if args.fields else ["id", "filename"]
        file_objs = list_file_objs(client)
        parsed_data = parse_file_objs(file_objs, fields)
        print(json.dumps(parsed_data, indent=4))

    elif args.action == "retrieve" and args.id:
        file_obj = retrieve_file(client, args.id)
        print(json.dumps(file_obj.__dict__, indent=4))

    elif args.action == "retrieve_content" and args.id:
        try:
            content = retrieve_file_content(client, args.id)
            print(content)  # Assuming content is plain text or similar
        except Exception as e:
            print("Error: Unable to retrieve file content.")

    elif args.action == "delete" and args.id:
        response = delete_file(client, args.id)
        print(json.dumps(response.__dict__, indent=4))

    elif args.action == "delete_range":
        start_date = parse_date(args.start_date) if args.start_date else None
        end_date = parse_date(args.end_date) if args.end_date else None

        if not start_date or not end_date:
            logging.error(
                "Both start_date and end_date are required for delete_range action."
            )
            return

        file_objs = list_file_objs(client)
        files_to_delete = filter_fobjs_by_date_range(file_objs, start_date, end_date)
        file_ids_to_delete = [f.id for f in files_to_delete]
        delete_results = delete_files_batch(client, file_ids_to_delete)
        print(json.dumps(delete_results, indent=4))

    else:
        logging.error("Invalid arguments. Please check the usage.")


if __name__ == "__main__":
    main()
