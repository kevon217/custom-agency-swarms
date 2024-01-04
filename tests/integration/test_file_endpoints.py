import unittest
from pathlib import Path
from agency_swarm.util.oai import get_openai_client
from custom_agency_swarms.utils.file_helper import (
    upload_file,
    list_file_objs,
    retrieve_file,
    delete_file,
)


class TestFileEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = get_openai_client()
        cls.file_dir = Path(__file__).parent.absolute()
        cls.uploaded_file_ids = []

    def test_file_endpoints(self):
        # Upload files
        dummy_init_file_id = upload_file(
            self.client, self.file_dir / "dummy_init.txt", "assistants"
        )
        dummy_add_file_id = upload_file(
            self.client, self.file_dir / "dummy_add.txt", "assistants"
        )
        dummy_del_file_id = upload_file(
            self.client, self.file_dir / "dummy_del.txt", "assistants"
        )
        self.uploaded_file_ids = [
            dummy_init_file_id,
            dummy_add_file_id,
            dummy_del_file_id,
        ]

        # List and verify files
        all_file_objs = list_file_objs(self.client)
        for file_id in self.uploaded_file_ids:
            self.assertTrue(
                any(fobj.id == file_id for fobj in all_file_objs),
                f"Uploaded file {file_id} not found in the list",
            )

        # Retrieve and verify file details
        for file_id in self.uploaded_file_ids:
            file_info = retrieve_file(self.client, file_id)
            self.assertEqual(
                file_info.id, file_id, f"Retrieved file ID does not match {file_id}"
            )

        # Cleanup: Delete the uploaded files
        for file_id in self.uploaded_file_ids:
            delete_file(self.client, file_id)


if __name__ == "__main__":
    unittest.main()
