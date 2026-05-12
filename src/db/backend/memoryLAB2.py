#База данных,содержащая в себе информацию о продаваемых на портале недвижимости квартир(идентификационный номер,кол-во комнат,
#адрес,содержащий название улицы и номер дома,а также площадь (кв.м) и стоимость квартиры(млн))

type FlatRecord=tuple[int,int,str,int,float,int]
Flat: list[FlatRecord]=[]
def create_record(
    flat_id: int,
    rooms_amount: int,
    street: str,
    house_number: int,
    square: float,
    cost: float,
) -> FlatRecord:
    if any(record[0]==flat_id for record in FlatRecord): #ошибки
        raise ValueError(f"Запись с ID {flat_id} уже существует")
    if rooms_amount<1:
        raise ValueError("Поле кол-ва комнат не может содержать значение менее 1")
    if house_number<1:
        raise ValueError("Поле номера дома не может содержать значение менее 1")
    if square<0:
        raise ValueError("Поле площади квартиры не может содержать значение менее 0")
    if cost<0:
        raise ValueError("Поле стоимости квартиры не может содержать значение менее 0")
    new_record: FlatRecord = (
        flat_id,
        rooms_amount,
        street,
        house_number,
        square,
        cost
    )
    Flat.append(new_record)
    return new_record

#чтение записей

def select_record(
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
        return Flat.copy()
    result:list[FlatRecord]=[]
    for record in Flat:
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
    flat_id: int,
    rooms_amount: int | None = None,
    street: str | None = None,
    house_number: int | None = None,
    square: float | None = None,
    cost: float | None = None,
) -> FlatRecord:
    for i,record in enumerate(Flat):
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
                flat_id,
                new_rooms_amount,
                new_street,
                new_house_number,
                new_square,
                new_cost,
            )
            Flat[i]=upd
            return upd

    raise ValueError(f"Запись с id={flat_id} не найдена")
def delete_record(flat_id: int) -> FlatRecord:
    for i,record in enumerate(Flat):
        if record[0]==flat_id:
            deleted=Flat.pop(i)
            return deleted
    raise ValueError(f"Запись с id={flat_id} не найдена")







    
  
