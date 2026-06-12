import csv
from pathlib import Path
from typing import Optional
from src2.errorsLAB4 import *


type FlatRecord = tuple[int, int, str, int, float, float]


class CSVStorage:
    
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._table_name = "flats"
        self._file_path = self.data_dir / f"{self._table_name}.csv"
        self._flats: list[FlatRecord] = []
        self._load()
    
    def _get_table_path(self) -> Path:
        return self._file_path
    
    def _table_exists(self) -> bool:
        return self._get_table_path().exists()
    
    def _load(self) -> None:
        if not self._table_exists():
            return
        
        try:
            with open(self._file_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                
                # Проверка заголовка (как в методичке)
                if header is None:
                    raise InvalidStorageDataError(f"Файл {self._table_name}.csv пуст или имеет некорректную структуру")
                
                for row in reader:
                    if len(row) == 6:
                        self._flats.append((
                            int(row[0]),    # id
                            int(row[1]),    # rooms
                            row[2],         # street
                            int(row[3]),    # house
                            float(row[4]),  # square
                            float(row[5])   # cost
                        ))
        except Exception as e:
            raise InvalidStorageDataError(f"Ошибка чтения CSV файла {self._table_name}.csv: {e}")
    
    def _save(self) -> None:
        with open(self._file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "rooms", "street", "house", "square", "cost"])
            for record in self._flats:
                writer.writerow(record)
    
    def create_record(
        self,
        flat_id: int,
        rooms_amount: int,
        street: str,
        house_number: int,
        square: float,
        cost: float
    ) -> FlatRecord:
        if rooms_amount < 1:
            raise InvalidRoomsAmountError("Поле кол-ва комнат не может содержать значение менее 1")
        if house_number < 1:
            raise InvalidHouseNumberError("Поле номера дома не может содержать значение менее 1")
        if square < 0:
            raise InvalidSquareError("Поле площади квартиры не может содержать значение менее 0")
        if cost < 0:
            raise InvalidCostError("Поле стоимости квартиры не может содержать значение менее 0")
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
        for i, record in enumerate(self._flats):
            if record[0] == flat_id:
                new_rooms = rooms_amount if rooms_amount is not None else record[1]
                new_street = street if street is not None else record[2]
                new_house = house_number if house_number is not None else record[3]
                new_square = square if square is not None else record[4]
                new_cost = cost if cost is not None else record[5]
                
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
        
        raise TableNotFoundError(f"Запись с ID {flat_id} не найдена в таблице {self._table_name}")
    
    def delete_record(self, flat_id: int) -> FlatRecord:

        for i, record in enumerate(self._flats):
            if record[0] == flat_id:
                deleted = self._flats.pop(i)
                self._save()
                return deleted
        raise TableNotFoundError(f"Запись с ID {flat_id} не найдена в таблице {self._table_name}")