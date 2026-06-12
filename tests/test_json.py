import unittest
import tempfile
import json
from pathlib import Path
from src2.json_storage import JSONStorage
from src2.errorsLAB4 import DuplicateIDError, InvalidStorageDataError,TableNotFoundError

class TestJSONStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = JSONStorage(self.temp_dir.name)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_create_and_select(self):
        self.storage.create_record(1, 2, "Test St", 10, 50.5, 100.0)
        self.storage.create_record(2, 3, "Another St", 20, 60.0, 200.0)
        
        all_records = self.storage.select_record()
        self.assertEqual(len(all_records), 2)
        
        filtered = self.storage.select_record(rooms_amount=2)
        self.assertEqual(len(filtered), 1)
    
    def test_persistence(self):
        self.storage.create_record(1, 2, "Persistent St", 5, 30.0, 150.0)
        
        new_storage = JSONStorage(self.temp_dir.name)
        records = new_storage.select_record()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][2], "Persistent St")
    
    def test_update(self):
        self.storage.create_record(1, 2, "Old", 10, 50, 100)
        self.storage.update_record(1, street="New", cost=150)
        
        records = self.storage.select_record(flat_id=1)
        self.assertEqual(records[0][2], "New")
        self.assertEqual(records[0][5], 150)
    
    def test_update_nonexist_record(self):
        with self.assertRaises(TableNotFoundError):
            self.storage.update_record(999, street="New")
    
    def test_delete(self):
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        self.storage.create_record(2, 3, "Test2", 20, 60, 200)
        
        self.storage.delete_record(1)
        records = self.storage.select_record()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][0], 2)
    
    def test_delete_nonexist_record(self):
        with self.assertRaises(TableNotFoundError):
            self.storage.delete_record(999)
    
    def test_duplicate_id(self):
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        with self.assertRaises(DuplicateIDError):
            self.storage.create_record(1, 3, "Test2", 20, 60, 200)
    
    def test_corrupted_json(self):
        json_path = Path(self.temp_dir.name) / "flats.json"
        json_path.write_text("{ invalid json ", encoding="utf-8")
        
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(self.temp_dir.name)
    
    def test_invalid_structure(self):
        json_path = Path(self.temp_dir.name) / "flats.json"
        json_path.write_text('{"wrong_key": []}', encoding="utf-8")
        
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(self.temp_dir.name)