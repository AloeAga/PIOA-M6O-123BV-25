"""In-memory реализация базы данных."""

from src.db.backend.database import Database
from src.db.backend.errors import (
    InvalidRoomsAmountError,
    InvalidHouseNumberError,
    InvalidSquareError,
    InvalidCostError,
    DuplicateIDError
)

type FlatRecord = tuple[int, int, str, int, float, float]


class FlatTable(Database):
    """Таблица для хранения квартир в оперативной памяти."""
    
    def __init__(self) -> None:
        self._flats: list[FlatRecord] = []

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
        
        new_record: FlatRecord = (flat_id, rooms_amount, street.strip(), house_number, square, cost)
        self._flats.append(new_record)
        return new_record

    def select_record(
        self,
        flat_id: int | None = None,
        rooms_amount: int | None = None,
        street: str | None = None,
        house_number: int | None = None,
        square: float | None = None,
        cost: float | None = None,
    ) -> list[FlatRecord]:
        if all(param is None for param in [flat_id, rooms_amount, street, house_number, square, cost]):
            return self._flats.copy()
        
        result: list[FlatRecord] = []
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
        rooms_amount: int | None = None,
        street: str | None = None,
        house_number: int | None = None,
        square: float | None = None,
        cost: float | None = None,
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

                updated: FlatRecord = (flat_id, new_rooms, new_street, new_house, new_square, new_cost)
                self._flats[i] = updated
                return updated
        
        raise ValueError(f"Запись с ID {flat_id} не найдена")

    def delete_record(self, flat_id: int) -> FlatRecord:
        for i, record in enumerate(self._flats):
            if record[0] == flat_id:
                return self._flats.pop(i)
        raise ValueError(f"Запись с ID {flat_id} не найдена")
    
    def clear(self) -> None:
        """Очищает все записи."""
        self._flats.clear()
    
    def get_all(self) -> list[FlatRecord]:
        """Возвращает копию всех записей."""
        return self._flats.copy()
    
    def __len__(self) -> int:
        return len(self._flats)