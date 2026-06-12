import unittest
import tempfile
import csv
from pathlib import Path

from src.db.backend.csv_storage import CSVStorage
from src.db.backend.errors import (
    DuplicateIDError,
    InvalidStorageDataError,
    TableNotFoundError,
    InvalidRoomsAmountError,
    InvalidHouseNumberError,
    InvalidSquareError,
    InvalidCostError
)


class TestCSVStorage(unittest.TestCase):
    """Полные тесты для CSV хранилища."""
    
    def setUp(self):
        """Создаёт временную директорию для тестов."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage = CSVStorage(self.temp_dir.name)
    
    def tearDown(self):
        """Очищает временную директорию."""
        self.temp_dir.cleanup()
    
    # ========== 1. ТЕСТЫ СОЗДАНИЯ И СОХРАНЕНИЯ ==========
    
    def test_create_record(self):
        """Тест создания записи."""
        record = self.storage.create_record(1, 2, "CSV St", 15, 45.0, 120.0)
        
        # Проверяем, что запись создалась с правильными данными
        self.assertEqual(record, (1, 2, "CSV St", 15, 45.0, 120.0))
        
        # Проверяем, что запись добавилась в хранилище
        all_records = self.storage.select_record()
        self.assertEqual(len(all_records), 1)
        self.assertEqual(all_records[0], (1, 2, "CSV St", 15, 45.0, 120.0))
    
    def test_create_and_select_all(self):
        """Тест создания нескольких записей и выборки всех."""
        self.storage.create_record(1, 2, "First St", 10, 50.0, 100.0)
        self.storage.create_record(2, 3, "Second St", 20, 60.0, 200.0)
        self.storage.create_record(3, 4, "Third St", 30, 70.0, 300.0)
        
        all_records = self.storage.select_record()
        
        # Проверяем количество записей
        self.assertEqual(len(all_records), 3)
        
        # Проверяем содержимое
        self.assertEqual(all_records[0], (1, 2, "First St", 10, 50.0, 100.0))
        self.assertEqual(all_records[1], (2, 3, "Second St", 20, 60.0, 200.0))
        self.assertEqual(all_records[2], (3, 4, "Third St", 30, 70.0, 300.0))
    
    # ========== 2. ТЕСТЫ ФИЛЬТРАЦИИ ==========
    
    def test_select_with_filter_by_id(self):
        """Тест фильтрации по ID."""
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        self.storage.create_record(2, 3, "Second", 20, 60, 200)
        self.storage.create_record(3, 4, "Third", 30, 70, 300)
        
        records = self.storage.select_record(flat_id=2)
        
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][0], 2)
        self.assertEqual(records[0][2], "Second")
    
    def test_select_with_filter_by_rooms(self):
        """Тест фильтрации по количеству комнат."""
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        self.storage.create_record(2, 3, "Second", 20, 60, 200)
        self.storage.create_record(3, 2, "Third", 30, 70, 300)
        
        records = self.storage.select_record(rooms_amount=2)
        
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0][0], 1)
        self.assertEqual(records[1][0], 3)
    
    def test_select_with_multiple_filters(self):
        """Тест фильтрации по нескольким полям."""
        self.storage.create_record(1, 2, "Main St", 10, 50, 100)
        self.storage.create_record(2, 2, "Main St", 20, 60, 200)
        self.storage.create_record(3, 3, "Other St", 10, 50, 100)
        
        # Ищем: 2 комнаты, улица Main St, дом 10
        records = self.storage.select_record(
            rooms_amount=2,
            street="Main St",
            house_number=10
        )
        
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][0], 1)
    
    def test_select_no_filters_returns_all(self):
        """Тест: без фильтров возвращаются все записи."""
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        self.storage.create_record(2, 3, "Second", 20, 60, 200)
        
        records = self.storage.select_record()
        
        self.assertEqual(len(records), 2)
    
    def test_select_empty_result(self):
        """Тест: фильтр не находит записей."""
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        
        records = self.storage.select_record(rooms_amount=5)
        
        self.assertEqual(len(records), 0)
    
    # ========== 3. ТЕСТЫ СОХРАНЕНИЯ МЕЖДУ ЗАПУСКАМИ (PERSISTENCE) ==========
    
    def test_persistence_between_instances(self):
        """Тест: данные сохраняются между разными экземплярами (ключевой тест!)."""
        # Первый экземпляр — создаём записи
        self.storage.create_record(1, 2, "Persistent St", 5, 30.0, 150.0)
        self.storage.create_record(2, 3, "Another St", 10, 40.0, 200.0)
        
        # Второй экземпляр в той же директории — загружает данные
        new_storage = CSVStorage(self.temp_dir.name)
        records = new_storage.select_record()
        
        # Проверяем, что данные загрузились
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0][2], "Persistent St")
        self.assertEqual(records[1][2], "Another St")
    
    def test_file_created_on_disk(self):
        """Тест: файл действительно создаётся на диске."""
        csv_path = Path(self.temp_dir.name) / "flats.csv"
        
        # До создания записей файла может не быть (или он пустой)
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        
        # После создания записей файл должен существовать
        self.assertTrue(csv_path.exists())
        
        # Проверяем, что файл не пустой
        self.assertGreater(csv_path.stat().st_size, 0)
    
    def test_csv_has_correct_header(self):
        """Тест: CSV файл содержит правильный заголовок."""
        self.storage.create_record(1, 2, "Header Test", 1, 10.0, 100.0)
        
        csv_path = Path(self.temp_dir.name) / "flats.csv"
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
        
        expected_header = ["id", "rooms", "street", "house", "square", "cost"]
        self.assertEqual(header, expected_header)
    
    # ========== 4. ТЕСТЫ ОБНОВЛЕНИЯ ЗАПИСЕЙ ==========
    
    def test_update_record(self):
        """Тест обновления записи."""
        self.storage.create_record(1, 2, "Old Street", 10, 50, 100)
        
        updated = self.storage.update_record(1, street="New Street", cost=150)
        
        # Проверяем возвращённое значение
        self.assertEqual(updated[2], "New Street")
        self.assertEqual(updated[5], 150)
        
        # Проверяем, что запись действительно обновилась в хранилище
        records = self.storage.select_record(flat_id=1)
        self.assertEqual(records[0][2], "New Street")
        self.assertEqual(records[0][5], 150)
    
    def test_update_nonexistent_record(self):
        """Тест обновления несуществующей записи."""
        with self.assertRaises(TableNotFoundError):
            self.storage.update_record(999, street="New")
    
    def test_update_partial_fields(self):
        """Тест обновления только некоторых полей."""
        self.storage.create_record(1, 2, "Original", 10, 50, 100)
        
        # Обновляем только стоимость
        self.storage.update_record(1, cost=200)
        
        records = self.storage.select_record(flat_id=1)
        self.assertEqual(records[0][2], "Original")  # Улица не изменилась
        self.assertEqual(records[0][5], 200)         # Стоимость изменилась
    
    # ========== 5. ТЕСТЫ УДАЛЕНИЯ ЗАПИСЕЙ ==========
    
    def test_delete_record(self):
        """Тест удаления записи."""
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        self.storage.create_record(2, 3, "Test2", 20, 60, 200)
        
        deleted = self.storage.delete_record(1)
        
        # Проверяем удалённую запись
        self.assertEqual(deleted[0], 1)
        
        # Проверяем, что запись удалена из хранилища
        remaining = self.storage.select_record()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0][0], 2)
    
    def test_delete_nonexistent_record(self):
        """Тест удаления несуществующей записи."""
        with self.assertRaises(TableNotFoundError):
            self.storage.delete_record(999)
    
    def test_delete_persistence(self):
        """Тест: удаление сохраняется в файле."""
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        self.storage.delete_record(1)
        
        # Создаём новый экземпляр — запись должна отсутствовать
        new_storage = CSVStorage(self.temp_dir.name)
        records = new_storage.select_record()
        self.assertEqual(len(records), 0)
    
    # ========== 6. ТЕСТЫ ВАЛИДАЦИИ ОШИБОК ==========
    
    def test_duplicate_id_error(self):
        """Тест ошибки дублирования ID."""
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        
        with self.assertRaises(DuplicateIDError):
            self.storage.create_record(1, 3, "Second", 20, 60, 200)
    
    def test_invalid_rooms_amount(self):
        """Тест ошибки: неверное количество комнат."""
        with self.assertRaises(InvalidRoomsAmountError):
            self.storage.create_record(1, 0, "Test", 10, 50, 100)
        
        with self.assertRaises(InvalidRoomsAmountError):
            self.storage.create_record(1, -5, "Test", 10, 50, 100)
    
    def test_invalid_house_number(self):
        """Тест ошибки: неверный номер дома."""
        with self.assertRaises(InvalidHouseNumberError):
            self.storage.create_record(1, 2, "Test", 0, 50, 100)
        
        with self.assertRaises(InvalidHouseNumberError):
            self.storage.create_record(1, 2, "Test", -10, 50, 100)
    
    def test_invalid_square(self):
        """Тест ошибки: неверная площадь."""
        with self.assertRaises(InvalidSquareError):
            self.storage.create_record(1, 2, "Test", 10, -50, 100)
    
    def test_invalid_cost(self):
        """Тест ошибки: неверная стоимость."""
        with self.assertRaises(InvalidCostError):
            self.storage.create_record(1, 2, "Test", 10, 50, -100)
    
    def test_empty_csv_file(self):
        """Тест: пустой CSV файл не вызывает ошибку."""
        csv_path = Path(self.temp_dir.name) / "flats.csv"
        csv_path.write_text("", encoding="utf-8")
        storage = CSVStorage(self.temp_dir.name)
        records = storage.select_record()
        self.assertEqual(len(records), 0)
    
    def test_corrupted_csv_file(self):
        csv_path = Path(self.temp_dir.name) / "flats.csv"
        csv_path.write_text("This is not a valid CSV file\ncorrupted data", encoding="utf-8")
        
        # Должен выбросить исключение
        with self.assertRaises(InvalidStorageDataError):
            CSVStorage(self.temp_dir.name)   
    def test_clear_method(self):
        """Тест очистки всех записей."""
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        self.storage.create_record(2, 3, "Second", 20, 60, 200)
        self.assertEqual(len(self.storage), 2)
        
        self.storage.clear()
        self.assertEqual(len(self.storage), 0)
        
        # Проверяем, что файл тоже очистился
        new_storage = CSVStorage(self.temp_dir.name)
        self.assertEqual(len(new_storage), 0)

    
    def test_get_all_returns_copy(self):
        """Тест: get_all возвращает копию, а не оригинал."""
        self.storage.create_record(1, 2, "Test", 10, 50, 100)
        
        records = self.storage.get_all()
        records.append((99, 1, "Fake", 1, 1, 1))
        
        # Оригинал не должен измениться
        self.assertEqual(len(self.storage), 1)
    def test_len_method(self):
        self.assertEqual(len(self.storage), 0)
        
        self.storage.create_record(1, 2, "First", 10, 50, 100)
        self.assertEqual(len(self.storage), 1)
        
        self.storage.create_record(2, 3, "Second", 20, 60, 200)
        self.assertEqual(len(self.storage), 2)
if __name__ == "__main__":
    unittest.main()