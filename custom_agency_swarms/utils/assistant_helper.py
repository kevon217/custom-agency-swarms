import logging

## ASSISTANT MANAGEMENT ##


def list_assistants(client, order="desc", limit=20):
    logging.info("Listing assistants...")
    response = client.beta.assistants.list(order=order, limit=limit)
    logging.info("Successfully listed assistants.")
    return response.data


def inspect_assistants(assistants):
    """
    Uses currying to create a two-step function for inspecting assistants.
    The outer function takes a list of assistant objects and returns an inner function.
    The inner function, when called with specific keys, returns data for those keys from each assistant object.
    If no keys are provided, it defaults to returning all data from the assistant objects.

    Usage:
    - First call: `inspect_func = inspect_assistants(assistants)`
    - Second call: `inspect_func(['id', 'name'])` or `inspect_func()` for all data

    Args:
    assistants (list): List of assistant objects.

    Returns:
    Function: A function that when called with keys, returns processed data for those keys.
    """
    logging.info("Inspecting assistants...")

    def inspect_keys(keys=None):
        processed_data = []
        for assistant in assistants:
            if keys:
                processed_info = {key: getattr(assistant, key, "") for key in keys}
            else:
                processed_info = vars(assistant)
            processed_data.append(processed_info)
        logging.info("Successfully inspected assistants.")
        return processed_data

    return inspect_keys


def create_assistant(client, name, instructions, model, tools):
    logging.info(f"Creating a new assistant: {name}")
    try:
        assistant = client.beta.assistants.create(
            instructions=instructions, name=name, tools=tools, model=model
        )
        logging.info(f"Assistant created successfully: {assistant.id}")
        return assistant
    except Exception as e:
        logging.error(f"Error creating assistant: {e}")
        raise


def create_assistant_file(client, assistant_id, file_id):
    logging.info(f"Creating file for assistant ID: {assistant_id}")
    try:
        assistant_file = client.beta.assistants.files.create(
            assistant_id=assistant_id, file_id=file_id
        )
        logging.info(f"File created successfully for assistant ID: {assistant_id}")
        return assistant_file
    except Exception as e:
        logging.error(f"Error creating file for assistant: {e}")
        raise


def retrieve_assistant(client, assistant_id):
    logging.info(f"Retrieving assistant with ID: {assistant_id}")
    try:
        assistant = client.beta.assistants.retrieve(assistant_id)
        logging.info(f"Assistant retrieved successfully: {assistant.id}")
        return assistant
    except Exception as e:
        logging.error(f"Error retrieving assistant: {e}")
        raise


def retrieve_assistant_by_name(client, name):
    logging.info(f"Retrieving assistant with name: {name}")
    try:
        all_assistants = list_assistants(client)
        for assistant in all_assistants:
            if assistant.name == name:
                logging.info(f"Assistant found: {assistant.id}")
                return assistant
        logging.warning(f"No assistant found with name: {name}")
    except Exception as e:
        logging.error(f"Error retrieving assistants: {e}")
        raise


def list_assistant_files(client, assistant_id):
    logging.info(f"Listing files for assistant ID: {assistant_id}")
    response = client.beta.assistants.files.list(assistant_id=assistant_id)
    logging.info("Successfully listed assistant files.")
    return response.data


def retrieve_assistant_file(client, assistant_id, file_id):
    logging.info(f"Retrieving file with ID: {file_id} for assistant ID: {assistant_id}")
    try:
        assistant_file = client.beta.assistants.files.retrieve(
            assistant_id=assistant_id, file_id=file_id
        )
        logging.info(f"File retrieved successfully for assistant ID: {assistant_id}")
        return assistant_file
    except Exception as e:
        logging.error(f"Error retrieving file for assistant: {e}")
        raise


def delete_assistant_file(client, assistant_id, file_id):
    logging.info(f"Deleting file ID: {file_id} from assistant ID: {assistant_id}")
    try:
        response = client.beta.assistants.files.delete(
            assistant_id=assistant_id, file_id=file_id
        )
        if response.deleted:
            logging.info("Assistant file deleted successfully.")
        else:
            logging.warning(f"Failed to delete file: {file_id}")
        return response
    except Exception as e:
        logging.error(f"Error deleting file: {e}")
        raise


def update_assistant(client, assistant_id, **kwargs):
    logging.info(f"Modifying assistant ID: {assistant_id}")
    response = client.beta.assistants.update(assistant_id, **kwargs)
    logging.info("Assistant modified successfully.")
    return response


def delete_assistant(client, assistant_id):
    logging.info(f"Attempting to delete assistant ID: {assistant_id}")
    try:
        response = client.beta.assistants.delete(assistant_id=assistant_id)
        if response.deleted:
            logging.info(f"Assistant ID: {assistant_id} successfully deleted.")
        else:
            logging.warning(
                f"Assistant ID: {assistant_id} was not deleted. Response: {response}"
            )
        return response
    except Exception as e:
        logging.error(f"Error deleting assistant ID: {assistant_id}. Error: {e}")
        raise


def delete_assistants(client):
    logging.info("Preparing to delete multiple assistants...")

    def delete(ids):
        results = {"deleted": [], "failed": []}
        for assistant_id in ids:
            try:
                response = client.beta.assistants.delete(assistant_id=assistant_id)
                if response.deleted:
                    results["deleted"].append(assistant_id)
                    logging.info(f"Successfully deleted assistant ID: {assistant_id}")
                else:
                    results["failed"].append(assistant_id)
                    logging.warning(
                        f"Assistant ID: {assistant_id} was not deleted. Response: {response}"
                    )
            except Exception as e:
                results["failed"].append((assistant_id, str(e)))
                logging.error(
                    f"Error deleting assistant ID: {assistant_id}. Error: {e}"
                )

        return results

    return delete
