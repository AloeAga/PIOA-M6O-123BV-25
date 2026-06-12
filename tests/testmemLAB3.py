import unittest
import tempfile
from pathlib import Path

from src.db.backend.memory import FlatTable
from src.db.backend.json_storage import JSONStorage
from src.db.backend.csv_storage import CSVStorage
from src.db.backend.errors import (
    InvalidRoomsAmountError,
    InvalidHouseNumberError,
    InvalidSquareError,
    InvalidCostError,
    DuplicateIDError,
    TableNotFoundError,
    InvalidStorageDataError
)
class BaseStorageTest:
    """Базовый класс для тестирования хранилищ.
    
    Содержит общие тесты, которые должны проходить все реализации.
    """
    
    def setUp(self):
        """Создаёт экземпляр хранилища (переопределяется в дочерних классах)."""
        raise NotImplementedError
    
    def tearDown(self):
        """Очищает ресурсы (переопределяется в дочерних классах)."""
        pass
    
    def test_create_record(self):
        """Тест создания записи."""
        cases = [
            (1, 2, "Marble Avenue", 60, 48, 10.5),
            (2, 4, "Greenbloom Street", 22, 87, 48.3),
            (3, 1, "Campbell Street", 5, 31, 8.6),
            (4, 1, "Rollway Lane", 8, 26, 7.1),
            (5, 3, "Orange Cross", 29, 70, 26.5),
            (6, 2, "Tompson Street", 88, 54, 14.9),
            (7, 2, "Royal Cross", 40, 45.6, 17.7),
            (8, 2, "Limestone Avenue", 117, 38.3, 13.2),
            (9, 4, "Waldorf Lane", 1, 100.6, 66.2),
            (10, 2, "St Mary Road", 5, 40, 12.2),
            (11, 3, "Lovelace Lane", 2, 61, 43.5),
            (12, 2, "Redoak Road", 19, 50, 28),
            (13, 3, "Westwick Street", 52, 69, 42),
            (14, 5, "Pacific Avenue", 220, 122, 92.6),
            (15, 2, "Windblow Street", 132, 53, 20),
            (16, 1, "Medowbrook Highway", 44, 23, 4.7)
        ]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.storage.create_record(*test_data)
                self.assertEqual(record, test_data)
    
    def test_create_record_rooms_amount_below1(self):
        """Тест: ошибка при количестве комнат < 1."""
        cases = [
            (1, -2, "Marble Avenue", 60, 48, 10.5),
            (2, 0, "Greenbloom Street", 22, 87, 48.3),
            (3, -444, "Campbell Street", 5, 31, 8.6),
            (4, -1, "Rollway Lane", 8, 26, 7.1)
        ]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidRoomsAmountError):
                    self.storage.create_record(*test_data)
    
    def test_create_record_house_number_below1(self):
        """Тест: ошибка при номере дома < 1."""
        cases = [
            (1, 2, "Marble Avenue", -60, 48, 10.5),
            (2, 4, "Greenbloom Street", -22, 87, 48.3),
            (3, 1, "Campbell Street", 0, 31, 8.6),
            (4, 1, "Rollway Lane", -8, 26, 7.1),
        ]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidHouseNumberError):
                    self.storage.create_record(*test_data)
    
    def test_create_record_negative_square(self):
        """Тест: ошибка при отрицательной площади."""
        cases = [
            (1, 2, "Marble Avenue", 60, -48, 10.5),
            (2, 4, "Greenbloom Street", 22, -87, 48.3),
            (3, 1, "Campbell Street", 5, -31, 8.6),
            (4, 1, "Rollway Lane", 8, -26, 7.1)
        ]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidSquareError):
                    self.storage.create_record(*test_data)
    
    def test_create_record_negative_cost(self):
        """Тест: ошибка при отрицательной стоимости."""
        cases = [
            (1, 2, "Marble Avenue", 60, 48, -10.5),
            (2, 4, "Greenbloom Street", 22, 87, -48.3),
            (3, 1, "Campbell Street", 5, 31, -8.6),
            (4, 1, "Rollway Lane", 8, 26, -7.1)
        ]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidCostError):
                    self.storage.create_record(*test_data)
    
    def test_create_record_duplicate_id(self):
        """Тест: ошибка при дублировании ID."""
        test_data_1 = (1, 2, "Marble Avenue", 60, 48, 10.5)
        test_data_2 = (1, 4, "Greenbloom Street", 22, 87, 48.3)
        
        self.storage.create_record(*test_data_1)
        
        with self.assertRaises(DuplicateIDError):
            self.storage.create_record(*test_data_2)   
    def test_select_record(self):
        """Тест выборки записей с фильтрами."""
        test_datas = [
            (1, 2, "Marble Avenue", 60, 48, 10.5),
            (2, 4, "Greenbloom Street", 22, 87, 48.3),
            (3, 1, "Campbell Street", 5, 31, 8.6),
            (4, 1, "Rollway Lane", 8, 26, 7.1),
            (5, 3, "Orange Cross", 29, 70, 26.5),
            (6, 2, "Tompson Street", 88, 54, 14.9),
            (7, 2, "Royal Cross", 40, 45.6, 17.7),
            (8, 2, "Limestone Avenue", 117, 38.3, 13.2),
            (9, 4, "Waldorf Lane", 1, 100.6, 66.2),
            (10, 2, "St Mary Road", 5, 40, 12.2),
            (11, 3, "Lovelace Lane", 2, 61, 43.5),
            (12, 2, "Redoak Road", 19, 50, 28),
            (13, 3, "Westwick Street", 52, 69, 42),
            (14, 5, "Pacific Avenue", 220, 122, 92.6),
            (15, 2, "Windblow Street", 132, 53, 20),
            (16, 1, "Medowbrook Highway", 44, 23, 4.7)
        ]
        
        for test_data in test_datas:
            self.storage.create_record(*test_data)
        
        cases = [
            {
                "name": "Выбор без фильтров",
                "filters": {},
                "expected": test_datas,
            },
            {
                "name": "Фильтр по ID",
                "filters": {"flat_id": 1},
                "expected": [test_datas[0]],
            },
            {
                "name": "Фильтр по кол-ву комнат",
                "filters": {"rooms_amount": 3},
                "expected": [test_datas[4], test_datas[10], test_datas[12]],
            },
            {
                "name": "Фильтр по улице",
                "filters": {"street": "St Mary Road"},
                "expected": [test_datas[9]],
            },
            {
                "name": "Фильтр по номеру дома",
                "filters": {"house_number": 19},
                "expected": [test_datas[11]],
            },
            {
                "name": "Фильтр по площади",
                "filters": {"square": 122},
                "expected": [test_datas[13]],
            },
            {
                "name": "Фильтр по стоимости",
                "filters": {"cost": 13.2},
                "expected": [test_datas[7]],
            },
        ]
        for case in cases:
            with self.subTest(case=case["name"]):
                records = self.storage.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])    
    def test_update_record(self):
        """Тест обновления записи."""
        self.storage.create_record(1, 2, "Old Street", 10, 50, 100)
        
        updated = self.storage.update_record(1, street="New Street", cost=150)
        self.assertEqual(updated[2], "New Street")
        self.assertEqual(updated[5], 150)
        
        # Проверяем, что запись действительно обновилась
        records = self.storage.select_record(flat_id=1)
        self.assertEqual(records[0][2], "New Street")
        self.assertEqual(records[0][5], 150)
    
    def test_update_nonexistent_record(self):
        """Тест обновления несуществующей записи."""
        with self.assertRaises(ValueError):
            self.storage.update_record(999, street="New")    
    def test_delete_record(self):
        """Тест удаления записи."""
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        self.storage.create_record(2, 3, "Test2", 20, 60, 200)
        
        deleted = self.storage.delete_record(1)
        self.assertEqual(deleted[0], 1)
        
        remaining = self.storage.select_record()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0][0], 2)
    
    def test_delete_nonexistent_record(self):
        """Тест удаления несуществующей записи."""
        with self.assertRaises(ValueError):
            self.storage.delete_record(999)
class TestMemoryStorage(BaseStorageTest, unittest.TestCase):
    """Тесты для in-memory хранилища."""
    
    def setUp(self):
        self.storage = FlatTable()
        self.assertIsInstance(self.storage, FlatTable)
    
    def tearDown(self):
        self.storage.clear()
class TestJSONStorage(BaseStorageTest, unittest.TestCase):
    """Тесты для JSON хранилища."""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = JSONStorage(self.temp_dir.name)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_persistence(self):
        """Тест сохранения данных между запусками (ключевой тест для файловых БД)."""
        self.storage.create_record(1, 2, "Persistent St", 5, 30.0, 150.0)
        self.storage.create_record(2, 3, "Another St", 10, 40.0, 200.0)
        new_storage = JSONStorage(self.temp_dir.name)
        records = new_storage.select_record()
        
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0][2], "Persistent St")
        self.assertEqual(records[1][2], "Another St")
    
    def test_corrupted_json(self):
        """Тест обработки битого JSON файла."""
        json_path = Path(self.temp_dir.name) / "flats.json"
        json_path.write_text("{ invalid json ", encoding="utf-8")
        
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(self.temp_dir.name)
    
    def test_invalid_structure(self):
        """Тест некорректной структуры JSON."""
        json_path = Path(self.temp_dir.name) / "flats.json"
        json_path.write_text('{"wrong_key": []}', encoding="utf-8")
        
        with self.assertRaises(InvalidStorageDataError):
            JSONStorage(self.temp_dir.name)
class TestCSVStorage(BaseStorageTest, unittest.TestCase):
    """Тесты для CSV хранилища."""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = CSVStorage(self.temp_dir.name)
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_persistence(self):
        self.storage.create_record(1, 2, "Persistent CSV", 8, 35.0, 180.0)
        self.storage.create_record(2, 3, "Another CSV", 12, 45.0, 250.0)
        new_storage = CSVStorage(self.temp_dir.name)
        records = new_storage.select_record()
        
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0][2], "Persistent CSV")
        self.assertEqual(records[1][2], "Another CSV")
    
    def test_csv_has_header(self):
        self.storage.create_record(1, 2, "Header Test", 1, 10.0, 100.0)
        
        csv_path = Path(self.temp_dir.name) / "flats.csv"
        with open(csv_path, "r", encoding="utf-8") as f:
            header = f.readline().strip()
        
        self.assertEqual(header, "id,rooms,street,house,square,cost")
    
    def test_empty_csv_file(self):
        csv_path = Path(self.temp_dir.name) / "flats.csv"
        csv_path.write_text("", encoding="utf-8")
        
        storage = CSVStorage(self.temp_dir.name)
        records = storage.select_record()
        self.assertEqual(len(records), 0)
if __name__ == "__main__":
    unittest.main()
