import csv
from pathlib import Path
from typing import Optional

from .errors import (
    InvalidRoomsAmountError,
    InvalidHouseNumberError,
    InvalidSquareError,
    InvalidCostError,
    DuplicateIDError,
    InvalidStorageDataError,
    TableNotFoundError
)

type FlatRecord = tuple[int, int, str, int, float, float]


class CSVStorage:
    """Хранилище в CSV файле. Данные сохраняются в data/flats.csv."""
    
    # Ожидаемая структура таблицы (заголовок CSV)
    EXPECTED_HEADER = ["id", "rooms", "street", "house", "square", "cost"]
    
    def __init__(self, data_dir: str = "data") -> None:
        """Инициализирует CSV хранилище.
        
        Args:
            data_dir: Директория для хранения файла flats.csv
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "flats.csv"
        self._flats: list[FlatRecord] = []
        self._load()
    
    def _load(self) -> None:
        """Загружает данные из CSV файла с проверкой структуры и явной обработкой ошибок."""
        if not self.file_path.exists():
            return
        
        try:
            with open(self.file_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                
                # Проверка наличия заголовка
                if header is None:
                    raise InvalidStorageDataError(
                        f"Файл {self.file_path.name} пуст или имеет некорректную структуру"
                    )
                
                # Проверка соответствия заголовка ожидаемой структуре
                if header != self.EXPECTED_HEADER:
                    raise InvalidStorageDataError(
                        f"Файл {self.file_path.name} имеет некорректный заголовок.\n"
                        f"  Ожидалось: {self.EXPECTED_HEADER}\n"
                        f"  Получено: {header}"
                    )
                
                # Загрузка записей с проверкой типов
                for row_num, row in enumerate(reader, start=2):
                    if len(row) != 6:
                        raise InvalidStorageDataError(
                            f"Файл {self.file_path.name}, строка {row_num}: "
                            f"ожидается 6 полей, получено {len(row)}"
                        )
                    
                    try:
                        flat_id = int(row[0])
                        rooms = int(row[1])
                        street = row[2]
                        house = int(row[3])
                        square = float(row[4])
                        cost = float(row[5])
                    except ValueError as e:
                        raise InvalidStorageDataError(
                            f"Файл {self.file_path.name}, строка {row_num}: "
                            f"ошибка преобразования типа данных: {e}"
                        )
                    
                    self._flats.append((flat_id, rooms, street, house, square, cost))
        
        except InvalidStorageDataError:
            raise  # Пробрасываем уже созданную ошибку
        except PermissionError as e:
            raise InvalidStorageDataError(f"Нет доступа к файлу {self.file_path.name}: {e}")
        except OSError as e:
            raise InvalidStorageDataError(f"Ошибка ввода-вывода при чтении файла {self.file_path.name}: {e}")
        except Exception as e:
            raise InvalidStorageDataError(f"Неожиданная ошибка при чтении файла {self.file_path.name}: {e}")
    
    def _save(self) -> None:
        """Сохраняет данные в CSV файл с заголовком."""
        try:
            with open(self.file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.EXPECTED_HEADER)
                for record in self._flats:
                    writer.writerow(record)
        except PermissionError as e:
            raise InvalidStorageDataError(f"Нет доступа к файлу {self.file_path.name} для записи: {e}")
        except OSError as e:
            raise InvalidStorageDataError(f"Ошибка ввода-вывода при записи файла {self.file_path.name}: {e}")
    
    def create_record(
        self,
        flat_id: int,
        rooms_amount: int,
        street: str,
        house_number: int,
        square: float,
        cost: float
    ) -> FlatRecord:
        """Добавляет новую запись."""
        # Валидация входных данных
        if rooms_amount < 1:
            raise InvalidRoomsAmountError("Поле кол-ва комнат не может содержать значение менее 1")
        if house_number < 1:
            raise InvalidHouseNumberError("Поле номера дома не может содержать значение менее 1")
        if square < 0:
            raise InvalidSquareError("Поле площади квартиры не может содержать значение менее 0")
        if cost < 0:
            raise InvalidCostError("Поле стоимости квартиры не может содержать значение менее 0")
        
        # Проверка на дубликат ID
        if any(record[0] == flat_id for record in self._flats):
            raise DuplicateIDError(f"Запись с ID {flat_id} уже существует")
        
        new_record = (flat_id, rooms_amount, street.strip(), house_number, square, cost)
        self._flats.append(new_record)
        self._save()
        return new_record
    
    def select_record(
        self,
        flat_id: Optional[int] = None,
        rooms_amount: Optional[int] = None,
        street: Optional[str] = None,
        house_number: Optional[int] = None,
        square: Optional[float] = None,
        cost: Optional[float] = None,
    ) -> list[FlatRecord]:
        """Возвращает записи, удовлетворяющие фильтрам."""
        # Если фильтры не указаны, возвращаем все записи
        if all(p is None for p in [flat_id, rooms_amount, street, house_number, square, cost]):
            return self._flats.copy()
        
        result = []
        for record in self._flats:
            if flat_id is not None and record[0] != flat_id:
                continue
            if rooms_amount is not None and record[1] != rooms_amount:
                continue
            if street is not None and record[2] != street:
                continue
            if house_number is not None and record[3] != house_number:
                continue
            if square is not None and record[4] != square:
                continue
            if cost is not None and record[5] != cost:
                continue
            result.append(record)
        return result
    
    def update_record(
        self,
        flat_id: int,
        rooms_amount: Optional[int] = None,
        street: Optional[str] = None,
        house_number: Optional[int] = None,
        square: Optional[float] = None,
        cost: Optional[float] = None,
    ) -> FlatRecord:
        """Обновляет существующую запись."""
        for i, record in enumerate(self._flats):
            if record[0] == flat_id:
                # Берём новые значения или оставляем старые
                new_rooms = rooms_amount if rooms_amount is not None else record[1]
                new_street = street if street is not None else record[2]
                new_house = house_number if house_number is not None else record[3]
                new_square = square if square is not None else record[4]
                new_cost = cost if cost is not None else record[5]
                
                # Валидация новых значений
                if new_rooms < 1:
                    raise InvalidRoomsAmountError("Количество комнат не может быть менее 1")
                if new_house < 1:
                    raise InvalidHouseNumberError("Номер дома не может быть менее 1")
                if new_square < 0:
                    raise InvalidSquareError("Площадь не может быть отрицательной")
                if new_cost < 0:
                    raise InvalidCostError("Стоимость не может быть отрицательной")
                
                updated = (flat_id, new_rooms, new_street, new_house, new_square, new_cost)
                self._flats[i] = updated
                self._save()
                return updated
        
        raise TableNotFoundError(f"Запись с ID {flat_id} не найдена")
    
    def delete_record(self, flat_id: int) -> FlatRecord:
        """Удаляет запись."""
        for i, record in enumerate(self._flats):
            if record[0] == flat_id:
                deleted = self._flats.pop(i)
                self._save()
                return deleted
        
        raise TableNotFoundError(f"Запись с ID {flat_id} не найдена")
    
    def clear(self) -> None:
        """Очищает все записи."""
        self._flats.clear()
        self._save()
    
    def get_all(self) -> list[FlatRecord]:
        """Возвращает копию всех записей."""
        return self._flats.copy()
    
    def __len__(self) -> int:
        """Возвращает количество записей."""
        return len(self._flats)
    
    def __repr__(self) -> str:
        """Строковое представление хранилища."""
        return f"CSVStorage(file={self.file_path.name}, records={len(self._flats)})"