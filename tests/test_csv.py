import unittest
import tempfile
import csv
from pathlib import Path
from src2.csv_storage import CSVStorage
from src2.errorsLAB4 import DuplicateIDError


class TestCSVStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = CSVStorage(self.temp_dir.name)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_create_and_select(self):
        self.storage.create_record(1, 2, "CSV St", 15, 45.0, 120.0)