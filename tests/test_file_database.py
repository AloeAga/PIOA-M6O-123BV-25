# tests/test_file_database.py
import tempfile
import unittest

from src.db.backend.errors import TableNotFoundError
from src.db.backend.file import FileDatabase


class TestFileDatabase(unittest.TestCase):
    def test_data_is_saved_between_instances(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_db = FileDatabase(directory)
            first_db.create_table("flats", ("flat_id", "rooms_amount","street","house_number","square","cost"))
            first_db.insert_record(
                "flats",
                {"flat_id": 1, "rooms_amount": 2,"street": "Marble Avenue","house_number":60,"square":45,"cost":10.5},
            )

            second_db = FileDatabase(directory)
            records = second_db.select_records("flats")

            self.assertEqual(
                records,
                [{"flat_id": 1, "rooms_amount": 2,"street": "Marble Avenue","house_number":60,"square":45,"cost":10.5}],
            )

    def test_select_with_filters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("flats", ("flat_id", "rooms_amount","street","house_number","square","cost"))
            db.insert_record("flats", {"flat_id": 1, "rooms_amount": 2,"street": "Marble Avenue","house_number":60,"square":45,"cost":10.5})
            db.insert_record("flats", {"flat_id": 2, "rooms_amount": 4,"street": "Gillian Square","house_number":11,"square":109,"cost":85.9})

            records = db.select_records("flats", flat_id=2)

            self.assertEqual(
                records,
                [{"flat_id": 2, "rooms_amount": 4,"street": "Gillian Square","house_number":11,"square":109,"cost":85.9}],
            )

    def test_select_from_missing_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)

            with self.assertRaises(TableNotFoundError):
                db.select_records("flats")