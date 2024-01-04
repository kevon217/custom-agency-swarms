import unittest
from pathlib import Path
from agency_swarm.util.oai import get_openai_client
from custom_agency_swarms.utils.file_helper import upload_file, delete_file
from custom_agency_swarms.utils.assistant_helper import (
    create_assistant,
    create_assistant_file,
    update_assistant,
    retrieve_assistant,
    delete_assistant,
    list_assistant_files,
    delete_assistant_file,
)


class TestAssistantWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = get_openai_client()
        cls.file_dir = Path(__file__).parent.absolute()

        # Upload dummy files and store their IDs for cleanup
        cls.dummy_init_file_id = upload_file(
            cls.client, cls.file_dir / "dummy_init.txt", "assistants"
        )
        cls.dummy_add_file_id = upload_file(
            cls.client, cls.file_dir / "dummy_add.txt", "assistants"
        )
        cls.dummy_del_file_id = upload_file(
            cls.client, cls.file_dir / "dummy_del.txt", "assistants"
        )

    def test_assistant_workflow(self):
        # Create a dummy assistant
        assistant = create_assistant(
            self.client,
            "Dummy_Assistant",
            "Initial Instructions",
            "gpt-4",
            [{"type": "code_interpreter"}],
        )
        self.assertIsNotNone(assistant.id, "Assistant ID is None")

        # Create "dummy_orig.txt" file
        original_file = create_assistant_file(
            self.client, assistant.id, self.dummy_init_file_id
        )
        self.assertIsNotNone(original_file, "Failed to create original file")

        # Modify the assistant's instructions and add "dummy_add.txt", "dummy_del.txt"
        updated_assistant = update_assistant(
            self.client,
            assistant.id,
            instructions="New Instructions",
            file_ids=[
                self.dummy_init_file_id,
                self.dummy_add_file_id,
                self.dummy_del_file_id,
            ],
        )
        self.assertEqual(
            updated_assistant.instructions,
            "New Instructions",
            "Assistant modification failed",
        )

        # Verify the files were added
        assistant_file_objs = list_assistant_files(self.client, assistant.id)
        self.assertTrue(
            any(afobj.id == self.dummy_add_file_id for afobj in assistant_file_objs),
            "File dummy_add.txt not found",
        )
        self.assertTrue(
            any(afobj.id == self.dummy_del_file_id for afobj in assistant_file_objs),
            "File dummy_del.txt not found",
        )

        # Retrieve the assistant
        retrieved_assistant = retrieve_assistant(self.client, assistant.id)
        self.assertEqual(
            retrieved_assistant.id,
            assistant.id,
            "Retrieved assistant ID does not match",
        )

        # Delete the "dummy_del.txt" file
        delete_response = delete_assistant_file(
            self.client, assistant.id, self.dummy_del_file_id
        )
        self.assertTrue(delete_response.deleted, "File deletion failed")

        # Delete the assistant
        delete_response = delete_assistant(self.client, assistant.id)
        self.assertTrue(delete_response.deleted, "Assistant deletion failed")

        for file_id in [
            self.dummy_init_file_id,
            self.dummy_add_file_id,
            self.dummy_del_file_id,
        ]:
            delete_file(self.client, file_id)


if __name__ == "__main__":
    unittest.main()
