import json
import unittest
from unittest.mock import patch
from src.db.backend.json_storage import JSONStorage
from src.db.backend.errors import (
    InvalidRoomsAmountError, InvalidHouseNumberError, InvalidSquareError,
    InvalidCostError, DuplicateIDError, InvalidStorageDataError, TableNotFoundError
)

class TestJSONStorage(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.storage = JSONStorage(data_dir=self.dir)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, data):
        with open(f"{self.dir}/flats.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def test_create_and_get_all(self):
        r = self.storage.create_record(1, 2, "A", 1, 10, 10)
        self.assertEqual(r, (1, 2, "A", 1, 10, 10))
        self.assertEqual(len(self.storage), 1)

    def test_create_validation(self):
        with self.assertRaises(InvalidRoomsAmountError):
            self.storage.create_record(1, 0, "A", 1, 10, 10)
        with self.assertRaises(InvalidHouseNumberError):
            self.storage.create_record(1, 1, "A", 0, 10, 10)
        with self.assertRaises(InvalidSquareError):
            self.storage.create_record(1, 1, "A", 1, -1, 10)
        with self.assertRaises(InvalidCostError):
            self.storage.create_record(1, 1, "A", 1, 10, -1)

    def test_create_duplicate(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        with self.assertRaises(DuplicateIDError):
            self.storage.create_record(1, 2, "B", 2, 20, 20)

    def test_create_rolls_back_on_save_error(self):
        with patch.object(JSONStorage, "_save", side_effect=InvalidStorageDataError("x")):
            with self.assertRaises(InvalidStorageDataError):
                self.storage.create_record(1, 1, "A", 1, 10, 10)
        self.assertEqual(len(self.storage), 0)

    def test_select(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        self.storage.create_record(2, 3, "B", 2, 20, 20)
        self.assertEqual(len(self.storage.select_record()), 2)
        self.assertEqual(self.storage.select_record(flat_id=1)[0][0], 1)

    def test_update(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        updated = self.storage.update_record(1, street="B", cost=99)
        self.assertEqual(updated[2], "B")
        self.assertEqual(updated[5], 99)
        with self.assertRaises(TableNotFoundError):
            self.storage.update_record(999, street="X")

    def test_update_validation(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        with self.assertRaises(InvalidRoomsAmountError):
            self.storage.update_record(1, rooms_amount=0)
        with self.assertRaises(InvalidHouseNumberError):
            self.storage.update_record(1, house_number=0)
        with self.assertRaises(InvalidSquareError):
            self.storage.update_record(1, square=-1)
        with self.assertRaises(InvalidCostError):
            self.storage.update_record(1, cost=-1)

    def test_update_rolls_back_on_save_error(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        with patch.object(JSONStorage, "_save", side_effect=InvalidStorageDataError("x")):
            with self.assertRaises(InvalidStorageDataError):
                self.storage.update_record(1, street="B")
        self.assertEqual(self.storage.select_record(flat_id=1)[0][2], "A")

    def test_delete(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        self.storage.create_record(2, 3, "B", 2, 20, 20)
        deleted = self.storage.delete_record(1)
        self.assertEqual(deleted[0], 1)
        self.assertEqual(len(self.storage), 1)
        with self.assertRaises(TableNotFoundError):
            self.storage.delete_record(999)

    def test_delete_rolls_back_on_save_error(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        with patch.object(JSONStorage, "_save", side_effect=InvalidStorageDataError("x")):
            with self.assertRaises(InvalidStorageDataError):
                self.storage.delete_record(1)
        self.assertEqual(len(self.storage), 1)

    def test_clear(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        self.storage.clear()
        self.assertEqual(len(self.storage), 0)

    def test_repr(self):
        self.assertTrue("records=0" in repr(self.storage))

    def test_load_missing_file(self):
        JSONStorage(data_dir=self.dir)
        self.assertEqual(len(self.storage), 0)

    def test_load_bad_json(self):
        with open(f"{self.dir}/flats.json", "w", encoding="utf-8") as f:
            f.write("{not valid json")
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_root_not_dict(self):
        self._write([])
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_missing_columns(self):
        self._write({"records": []})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_missing_records(self):
        self._write({"columns": JSONStorage.COLUMNS})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_wrong_columns(self):
        self._write({"columns": ["a"], "records": []})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_records_not_list(self):
        self._write({"columns": JSONStorage.COLUMNS, "records": {}})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_record_not_list(self):
        self._write({"columns": JSONStorage.COLUMNS, "records": ["bad"]})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_record_wrong_length(self):
        self._write({"columns": JSONStorage.COLUMNS, "records": [[1, 2, 3]]})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_record_bad_type(self):
        self._write({"columns": JSONStorage.COLUMNS,
                     "records": [[1, "x", "A", 1, 10, 10]]})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_negative_value(self):
        self._write({"columns": JSONStorage.COLUMNS,
                     "records": [[1, -1, "A", 1, 10, 10]]})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_duplicate_id(self):
        self._write({"columns": JSONStorage.COLUMNS,
                     "records": [[1, 1, "A", 1, 10, 10], [1, 2, "B", 2, 20, 20]]})
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(data_dir=self.dir)

    def test_load_success(self):
        self._write({"columns": JSONStorage.COLUMNS,
                     "records": [[1, 2, "A", 1, 10, 10]]})
        s = JSONStorage(data_dir=self.dir)
        self.assertEqual(len(s), 1)

    def test_save_permission_error(self):
        with patch("builtins.open", side_effect=PermissionError):
            with self.assertRaises(InvalidStorageDataError):
                self.storage._save()

if __name__ == "__main__":
    unittest.main()