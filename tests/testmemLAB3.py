import unittest
from src.db.backend.memory import FlatTable
from src.db.backend.errors import (
    InvalidRoomsAmountError,
    InvalidHouseNumberError,
    InvalidSquareError,
    InvalidCostError,
    DuplicateIDError,
    TableNotFoundError
)
class TestMemory(unittest.TestCase):
    def setUp(self):
        """Создаёт новое хранилище перед каждым тестом."""
        self.storage = FlatTable()
        self.assertIsInstance(self.storage, FlatTable)
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
        test_data_1 = (1, 2, "Marble Avenue", 60, 48, 10.5)
        test_data_2 = (1, 4, "Greenbloom Street", 22, 87, 48.3)       
        self.storage.create_record(*test_data_1)        
        with self.assertRaises(DuplicateIDError):
            self.storage.create_record(*test_data_2) 
    def test_select_record(self):
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
        self.storage.create_record(1, 2, "Old Street", 10, 50, 100)        
        updated = self.storage.update_record(1, street="New Street", cost=150)
        self.assertEqual(updated[2], "New Street")
        self.assertEqual(updated[5], 150)
        records = self.storage.select_record(flat_id=1)
        self.assertEqual(records[0][2], "New Street")
        self.assertEqual(records[0][5], 150)   
    def test_update_record_partial(self):
        self.storage.create_record(1, 2, "Original", 10, 50, 100)
        updated = self.storage.update_record(1, cost=200)       
        self.assertEqual(updated[2], "Original")  # Улица не изменилась
        self.assertEqual(updated[5], 200)         # Стоимость изменилась   
    def test_update_nonexistent_record(self):
        with self.assertRaises(ValueError):
            self.storage.update_record(999, street="New")
    def test_delete_record(self):
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
    def test_clear(self):
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        self.storage.create_record(2, 3, "Test2", 20, 60, 200)
        self.assertEqual(len(self.storage), 2)       
        self.storage.clear()
        self.assertEqual(len(self.storage), 0)   
    def test_get_all(self):
        self.storage.create_record(1, 2, "Test", 10, 50, 100)       
        records = self.storage.get_all()
        self.assertEqual(len(records), 1)
        records.append((99, 1, "Fake", 1, 1, 1))
        self.assertEqual(len(self.storage), 1)   
    def test_len(self):
        self.assertEqual(len(self.storage), 0)        
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        self.assertEqual(len(self.storage), 1)       
        self.storage.create_record(2, 3, "Second", 20, 60, 200)
        self.assertEqual(len(self.storage), 2)    
    def test_repr(self):
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        repr_str = repr(self.storage)
        self.assertIn("FlatTable", repr_str)
        self.assertIn("records=1", repr_str)
if __name__ == "__main__":
    unittest.main()