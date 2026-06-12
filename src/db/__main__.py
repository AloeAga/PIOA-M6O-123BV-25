
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.db.__init__ import create_storage
from src.db.tui import Application


def print_banner() -> None:
    print("=" * 60)


def print_storage_info(storage_type: str, records_count: int) -> None:
    print("\n" + "-" * 40)
    
    if storage_type == "memory":
        print("Тип хранилища: In-memory")
        print("Внимание: данные НЕ сохраняются после выхода из программы")
    elif storage_type == "json":
        print("Тип хранилища: JSON")
        print("Файл: data/flats.json")
        print("Данные сохраняются на диск")
    elif storage_type == "csv":
        print("Тип хранилища: CSV")
        print("Файл: data/flats.csv")
        print("Данные сохраняются на диск")
    
    print(f"Загружено записей: {records_count}")
    print("-" * 40)


def select_storage_type() -> str:
    print("\nВЫБОР ТИПА ХРАНИЛИЩА")
    print("-" * 40)
    print("1. In-memory (данные НЕ сохраняются)")
    print("2. JSON файл (данные сохраняются)")
    print("3. CSV файл (данные сохраняются)")
    print("-" * 40)
    
    while True:
        choice = input("Ваш выбор (1-3): ").strip()
        
        if choice == "1":
            print("\nВыбрано in-memory хранилище")
            return "memory"
        elif choice == "2":
            print("\nВыбрано JSON хранилище (файл: data/flats.json)")
            return "json"
        elif choice == "3":
            print("\nВыбрано CSV хранилище (файл: data/flats.csv)")
            return "csv"
        else:
            print("Ошибка: введите 1, 2 или 3.")


def main() -> None:
    """Главная функция запуска приложения."""
    print_banner()

    storage_type = select_storage_type()
    
    try:
        storage = create_storage(storage_type)
        records_count = len(storage.select_record())
        print_storage_info(storage_type, records_count)
    except Exception as e:
        print(f"\nОшибка при инициализации хранилища: {e}")
        print("Запуск с in-memory хранилищем по умолчанию...")
        storage = create_storage("memory")
        records_count = len(storage.select_record())
        print_storage_info("memory", records_count)
    
    print("\n" + "=" * 60)
    input("Нажмите Enter для продолжения...")

    app = Application(storage)
    app.run()


if __name__ == "__main__":
    main()