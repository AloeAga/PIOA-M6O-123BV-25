import csv
import unittest
from unittest.mock import patch
from src.db.backend.csv_storage import CSVStorage
from src.db.backend.errors import (
    InvalidRoomsAmountError, InvalidHouseNumberError, InvalidSquareError,
    InvalidCostError, DuplicateIDError, InvalidStorageDataError, TableNotFoundError
)

class TestCSVStorage(unittest.TestCase):
    def setUp(self):
        import tempfile, pathlib
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.storage = CSVStorage(data_dir=self.dir)

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_and_get_all(self):
        r = self.storage.create_record(1, 2, "A", 1, 10, 10)
        self.assertEqual(r, (1, 2, "A", 1, 10, 10))
        self.assertEqual(len(self.storage), 1)
        self.assertEqual(self.storage.get_all(), [(1, 2, "A", 1, 10, 10)])

    def test_create_strips_street(self):
        r = self.storage.create_record(1, 2, "  A  ", 1, 10, 10)
        self.assertEqual(r[2], "A")

    def test_create_duplicate(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        with self.assertRaises(DuplicateIDError):
            self.storage.create_record(1, 2, "B", 2, 20, 20)

    def test_create_validation(self):
        with self.assertRaises(InvalidRoomsAmountError):
            self.storage.create_record(1, 0, "A", 1, 10, 10)
        with self.assertRaises(InvalidHouseNumberError):
            self.storage.create_record(1, 1, "A", 0, 10, 10)
        with self.assertRaises(InvalidSquareError):
            self.storage.create_record(1, 1, "A", 1, -1, 10)
        with self.assertRaises(InvalidCostError):
            self.storage.create_record(1, 1, "A", 1, 10, -1)

    def test_create_rolls_back_on_save_error(self):
        with patch.object(CSVStorage, "_save", side_effect=InvalidStorageDataError("x")):
            with self.assertRaises(InvalidStorageDataError):
                self.storage.create_record(1, 1, "A", 1, 10, 10)
        self.assertEqual(len(self.storage), 0)

    def test_select(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        self.storage.create_record(2, 3, "B", 2, 20, 20)
        self.assertEqual(len(self.storage.select_record()), 2)
        self.assertEqual(self.storage.select_record(flat_id=1)[0][0], 1)
        self.assertEqual(self.storage.select_record(rooms_amount=3)[0][0], 2)
        self.assertEqual(self.storage.select_record(street="A")[0][0], 1)
        self.assertEqual(self.storage.select_record(house_number=2)[0][0], 2)
        self.assertEqual(self.storage.select_record(square=10)[0][0], 1)
        self.assertEqual(self.storage.select_record(cost=20)[0][0], 2)

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
        with patch.object(CSVStorage, "_save", side_effect=InvalidStorageDataError("x")):
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
        with patch.object(CSVStorage, "_save", side_effect=InvalidStorageDataError("x")):
            with self.assertRaises(InvalidStorageDataError):
                self.storage.delete_record(1)
        self.assertEqual(len(self.storage), 1)

    def test_clear(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        self.storage.clear()
        self.assertEqual(len(self.storage), 0)

    def test_clear_rolls_back_on_save_error(self):
        self.storage.create_record(1, 2, "A", 1, 10, 10)
        with patch.object(CSVStorage, "_save", side_effect=InvalidStorageDataError("x")):
            with self.assertRaises(InvalidStorageDataError):
                self.storage.clear()
        self.assertEqual(len(self.storage), 1)

    def test_repr(self):
        self.assertEqual("records=0" in repr(self.storage), True)

    def test_load_missing_file(self):
        CSVStorage(data_dir=self.dir)
        self.assertEqual(len(self.storage), 0)

    def test_load_bad_header(self):
        with open(f"{self.dir}/flats.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["wrong", "header"])
        with self.assertRaises(InvalidStorageDataError):
            CSVStorage(data_dir=self.dir)

    def test_load_bad_field_count(self):
        with open(f"{self.dir}/flats.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(CSVStorage.EXPECTED_HEADER)
            w.writerow([1, 2, "A"])
        with self.assertRaises(InvalidStorageDataError):
            CSVStorage(data_dir=self.dir)

    def test_load_bad_type(self):
        with open(f"{self.dir}/flats.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(CSVStorage.EXPECTED_HEADER)
            w.writerow([1, "not_int", "A", 1, 10, 10])
        with self.assertRaises(InvalidStorageDataError):
            CSVStorage(data_dir=self.dir)

    def test_load_negative_value(self):
        with open(f"{self.dir}/flats.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(CSVStorage.EXPECTED_HEADER)
            w.writerow([1, -1, "A", 1, 10, 10])
        with self.assertRaises(InvalidStorageDataError):
            CSVStorage(data_dir=self.dir)

    def test_load_duplicate_id(self):
        with open(f"{self.dir}/flats.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(CSVStorage.EXPECTED_HEADER)
            w.writerow([1, 1, "A", 1, 10, 10])
            w.writerow([1, 2, "B", 2, 20, 20])
        with self.assertRaises(InvalidStorageDataError):
            CSVStorage(data_dir=self.dir)

    def test_load_success(self):
        with open(f"{self.dir}/flats.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(CSVStorage.EXPECTED_HEADER)
            w.writerow([1, 2, "A", 1, 10, 10])
        s = CSVStorage(data_dir=self.dir)
        self.assertEqual(len(s), 1)

    def test_save_permission_error(self):
        with patch("builtins.open", side_effect=PermissionError):
            with self.assertRaises(InvalidStorageDataError):
                self.storage._save()

if __name__ == "__main__":
    unittest.main()