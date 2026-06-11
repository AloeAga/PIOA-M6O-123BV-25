# src/db/backend/memory.py
from .errorsLAB3 import InvalidRoomsAmountError,InvalidHouseNumberError,InvalidSquareError,InvalidCostError,DuplicateIDError 
type FlatRecord = tuple[int, str, str, int, str]

class FlatTable:
    def __init__(self) -> None:
        self._flat: list[FlatRecord] = []

    def create_record(
        self,
        flat_id: int,
        rooms_amount: int,
        street: str,
        house_number: int,
        square: float,
        cost: float
    ) -> FlatRecord:
        if rooms_amount<1:
            raise InvalidRoomsAmountError("Поле кол-ва комнат не может содержать значение менее 1")
        if house_number<1:
            raise InvalidHouseNumberError("Поле номера дома не может содержать значение менее 1")
        if square<0:
            raise InvalidSquareError("Поле площади квартиры не может содержать значение менее 0")
        if cost<0:
            raise InvalidCostError("Поле стоимости квартиры не может содержать значение менее 0")
        if any(record[0]==flat_id for record in self._flat):
            raise DuplicateIDError(f"Запись с ID {flat_id} уже существует")
        

        new_record: FlatRecord = (
            flat_id,
            rooms_amount,
            street.strip(),
            house_number,
            square,
            cost
        )
        self._flat.append(new_record)
        return new_record
    def select_record(
        self,
        flat_id: int | None=None,
        rooms_amount: int | None=None,
        street: str | None=None,
        house_number: int | None=None,
        square: float | None=None,
        cost: float | None=None,
    ) -> list[FlatRecord]:
        if(
            flat_id is None
            and rooms_amount is None
            and street is None
            and house_number is None
            and square is None
            and cost is None
        ):
            return self._flat.copy()
        result:list[FlatRecord]=[]
        for record in self._flat:
            if flat_id is not None and record[0]!=flat_id:
                continue
            if rooms_amount is not None and record[1]!=rooms_amount:
                continue
            if street is not None and record[2]!=street:
                continue
            if house_number is not None and record[3]!=house_number:
                continue
            if square is not None and record[4]!=square:
                continue
            if cost is not None and record[5]!=cost:
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
        for i,record in enumerate(self._flat):
            if record[0]==flat_id:
                new_rooms_amount=rooms_amount if rooms_amount is not None else record[1]
                new_street=street if street is not None else record[2]
                new_house_number=house_number if house_number is not None else record[3]
                new_square=square if square is not None else record[4]
                new_cost=cost if cost is not None else record[5]

                if new_rooms_amount<1:
                    raise ValueError("Поле кол-ва комнат не может содержать значение менее 1")
                if new_house_number<1:
                    raise ValueError("Поле номера дома не может содержать значение менее 1")
                if new_square<0:
                    raise ValueError("Поле площади квартиры не может содержать значение менее 0")
                if new_cost<0:
                    raise ValueError("Поле стоимости квартиры не может содержать значение менее 0")

                upd:FlatRecord=(
                    self,
                    flat_id,
                    new_rooms_amount,
                    new_street,
                    new_house_number,
                    new_square,
                    new_cost,
                )
                self._flat[i]=upd
                return upd
