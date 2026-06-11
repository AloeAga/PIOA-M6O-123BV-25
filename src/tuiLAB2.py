from src.db.backend.memoryLAB2 import create_record,select_record,update_record,delete_record

def print_menu() -> None:
    print("\n.~.~.~. База данных продаваемых квартир .~.~.~.")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("4. Обновить запись")
    print("5. Удалить запись")
    print("0. Выход")

def read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")

def read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите вещественное число.")

def add_flat() -> None:
    print("\nДобавление записи")
    flat_id=read_int("id: ")
    rooms_amount=read_int("rooms_amount: ")
    street=input("street: ").strip()
    house_number=read_int("house_number: ")
    square=read_float("square: ")
    cost=read_float("cost: ")
    try:
        record=create_record(flat_id,rooms_amount,street,house_number,square,cost)
        print(f"Запись добавлена: {record}")

    except ValueError as exc:
        print(f"Ошибка: {exc}")

def print_records(records: list[tuple[int,int,str,int,float,float]]) -> None:
    if not records:
        print("Запись не найдена")
        return
    
    for record in records:
        print(record)

def show_all() -> None:
    print("\nСписок записей")
    print_records(select_record())

def read_opt_int(prompt: str) -> int | None:
    while True:
        raw=input(prompt).strip()
        if raw=="":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")

def read_opt_float(prompt: str) -> float | None:
    while True:
        raw=input(prompt).strip()
        if raw=="":
            return None
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите вещественное число или оставьте поле пустым.")

def find_flat() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")
    flat_id=read_opt_int("id: ")
    rooms_amount=read_opt_int("rooms_amount :")
    street = input("street: ").strip() or None
    house_number = read_opt_int("house_number: ")
    square = read_opt_float("square: ")
    cost=read_opt_float("cost: ")

    records=select_record(
        flat_id=flat_id,
        rooms_amount=rooms_amount,
        street=street,
        house_number=house_number,
        square=square,
        cost=cost
    )
    print_records(records)

def update_flat() -> None:
    print("\nОбновление записи (Enter = оставить без изменений)")
    flat_id = read_int("id записи для обновления: ")

    print("Введите новые значения (Enter = пропустить):")
    rooms_amount = read_opt_int("rooms_amount: ")
    street = input("street: ").strip() or None
    house_number = read_opt_int("house_number: ")
    square = read_opt_float("square: ")
    cost = read_opt_float("cost: ")

    try:
        updated = update_record(
            flat_id=flat_id,
            rooms_amount=rooms_amount,
            street=street,
            house_number=house_number,
            square=square,
            cost=cost,
        )
        print(f"Запись обновлена: {updated}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")

def delete_flat() -> None:
    print("\nУдаление записи")
    flat_id=read_int("id записи для удаления: ")

    try:
        deleted=delete_record(flat_id)
        print(f"Запись удалена: {deleted}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")

def run() -> None:
    while True:
        print_menu()
        act=input("Выберите действие: ").strip()
        if act=="1":
            add_flat()
        elif act=="2":
            show_all()
        elif act=="3":
            find_flat()
        elif act=="4":
            update_flat()
        elif act=="5":
            delete_flat()
        elif act=="0":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")








