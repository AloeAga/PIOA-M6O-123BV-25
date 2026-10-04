import json
import os
from pathlib import Path
from src.db.backend.database import Database
from src.db.backend.errors import (
    InvalidRoomsAmountError, InvalidHouseNumberError,
    InvalidSquareError, InvalidCostError, DuplicateIDError,
    InvalidStorageDataError, TableNotFoundError
)
type FlatRecord = tuple[int, int, str, int, float, float]
def _validate(rooms, house, square, cost):
    if rooms < 1:
        raise InvalidRoomsAmountError(
            "Поле кол-ва комнат не может содержать значение менее 1"
        )
    if house < 1:
        raise InvalidHouseNumberError(
            "Поле номера дома не может содержать значение менее 1"
        )
    if square < 0:
        raise InvalidSquareError(
            "Поле площади квартиры не может содержать значение менее 0"
        )
    if cost < 0:
        raise InvalidCostError(
            "Поле стоимости квартиры не может содержать значение менее 0"
        )
class JSONStorage(Database):
    COLUMNS = ["id", "rooms", "street", "house", "square", "cost"]
    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "flats.json"
        self._flats: list[FlatRecord] = []
        self._load()
    def _load(self) -> None:
        if not self.file_path.exists():
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise InvalidStorageDataError(
                f"Файл {self.file_path.name} повреждён: "
                f"некорректный JSON.\n  Подробнее: {e}"
            )
        except (PermissionError, OSError) as e:
            raise InvalidStorageDataError(
                f"Ошибка чтения файла {self.file_path.name}: {e}"
            )
        if not isinstance(data, dict):
            raise InvalidStorageDataError(
                f"Файл {self.file_path.name}: "
                f"корень должен быть словарём"
            )
        if data.get("columns") != self.COLUMNS:
            raise InvalidStorageDataError(
                f"Файл {self.file_path.name} "
                f"имеет некорректные колонки"
            )
        if not isinstance(data.get("records"), list):
            raise InvalidStorageDataError(
                f"Файл {self.file_path.name}: "
                f"'records' должен быть списком"
            )
        loaded = []
        seen = set()
        for row_num, record in enumerate(data["records"], 1):
            if not isinstance(record, list) or len(record) != 6:
                raise InvalidStorageDataError(
                    f"Файл {self.file_path.name}, запись {row_num}: "
                    f"ожидается список из 6 полей"
                )
            try:
                flat_id = int(record[0])
                rooms = int(record[1])
                street = str(record[2])
                house = int(record[3])
                square = float(record[4])
                cost = float(record[5])
                _validate(rooms, house, square, cost)
            except (
                ValueError, TypeError,
                InvalidRoomsAmountError,
                InvalidHouseNumberError,
                InvalidSquareError,
                InvalidCostError
            ) as e:
                raise InvalidStorageDataError(
                    f"Файл {self.file_path.name}, запись {row_num}: "
                    f"некорректные данные: {e}"
                )
            if flat_id in seen:
                raise InvalidStorageDataError(
                    f"Файл {self.file_path.name}, запись {row_num}: "
                    f"дублирующийся ID {flat_id}"
                )
            seen.add(flat_id)
            loaded.append(
                (flat_id, rooms, street, house, square, cost)
            )
        self._flats = loaded
    def _save(self) -> None:
        temp_path = self.file_path.with_suffix(".tmp")
        data = {
            "columns": self.COLUMNS,
            "records": [list(record) for record in self._flats]
        }
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=2
                )
            os.replace(temp_path, self.file_path)
        except (PermissionError, OSError) as e:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise InvalidStorageDataError(
                f"Ошибка записи файла {self.file_path.name}: {e}"
            )
    def create_record(
        self, flat_id, rooms_amount, street,
        house_number, square, cost
    ) -> FlatRecord:
        _validate(
            rooms_amount,
            house_number,
            square,
            cost
        )
        if any(record[0] == flat_id for record in self._flats):
            raise DuplicateIDError(
                f"Запись с ID {flat_id} уже существует"
            )
        old = self._flats
        self._flats = old + [(
            flat_id,
            rooms_amount,
            street.strip(),
            house_number,
            square,
            cost
        )]
        try:
            self._save()
        except Exception:
            self._flats = old
            raise
        return self._flats[-1]
    def select_record(
        self, flat_id=None, rooms_amount=None,
        street=None, house_number=None,
        square=None, cost=None
    ) -> list[FlatRecord]:
        if all(p is None for p in [
            flat_id, rooms_amount, street,
            house_number, square, cost
        ]):
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
        self, flat_id, rooms_amount=None,
        street=None, house_number=None,
        square=None, cost=None
    ) -> FlatRecord:
        for i, record in enumerate(self._flats):
            if record[0] != flat_id:
                continue
            updated = (
                flat_id,
                rooms_amount if rooms_amount is not None else record[1],
                street.strip() if street is not None else record[2],
                house_number if house_number is not None else record[3],
                square if square is not None else record[4],
                cost if cost is not None else record[5]
            )
            _validate(
                updated[1],
                updated[3],
                updated[4],
                updated[5]
            )
            old = self._flats
            self._flats = (
                old[:i] + [updated] + old[i + 1:]
            )
            try:
                self._save()
            except Exception:
                self._flats = old
                raise
            return updated
        raise TableNotFoundError(
            f"Запись с ID {flat_id} не найдена"
        )
    def delete_record(self, flat_id: int) -> FlatRecord:
        for i, record in enumerate(self._flats):
            if record[0] != flat_id:
                continue
            old = self._flats
            self._flats = old[:i] + old[i + 1:]
            try:
                self._save()
            except Exception:
                self._flats = old
                raise
            return record
        raise TableNotFoundError(
            f"Запись с ID {flat_id} не найдена"
        )
    def clear(self) -> None:
        old = self._flats
        self._flats = []
        try:
            self._save()
        except Exception:
            self._flats = old
            raise
    def get_all(self) -> list[FlatRecord]:
        return self._flats.copy()
    def __len__(self) -> int:
        return len(self._flats)
    def __repr__(self) -> str:
        return (
            f"JSONStorage(file={self.file_path.name}, "
            f"records={len(self._flats)})"
        )