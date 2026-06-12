from typing import Optional, Any


class MenuPrinter:
    """Класс для отображения меню."""
    
    def print_menu(self) -> None:
        """Выводит главное меню программы."""
        print("\n.~.~.~. База данных продаваемых квартир .~.~.~.")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Найти записи по фильтру")
        print("4. Обновить запись")
        print("5. Удалить запись")
        print("0. Выход")


class InputValidator:
    """Класс для валидации пользовательского ввода."""
    
    @staticmethod
    def read_int(prompt: str) -> int:
        """
        Читает целое число с проверкой.
        
        Args:
            prompt: Текст приглашения для ввода
            
        Returns:
            Введённое целое число
        """
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")
    
    @staticmethod
    def read_float(prompt: str) -> float:
        """
        Читает вещественное число с проверкой.
        
        Args:
            prompt: Текст приглашения для ввода
            
        Returns:
            Введённое вещественное число
        """
        while True:
            raw = input(prompt).strip()
            try:
                return float(raw)
            except ValueError:
                print("Ошибка: введите вещественное число.")
    
    @staticmethod
    def read_opt_int(prompt: str) -> Optional[int]:
        """
        Читает опциональное целое число (можно оставить пустым).
        
        Args:
            prompt: Текст приглашения для ввода
            
        Returns:
            Введённое целое число или None, если поле пустое
        """
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым.")
    
    @staticmethod
    def read_opt_float(prompt: str) -> Optional[float]:
        """
        Читает опциональное вещественное число (можно оставить пустым).
        
        Args:
            prompt: Текст приглашения для ввода
            
        Returns:
            Введённое вещественное число или None, если поле пустое
        """
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return float(raw)
            except ValueError:
                print("Ошибка: введите вещественное число или оставьте поле пустым.")
    
    @staticmethod
    def read_string(prompt: str, required: bool = True) -> Optional[str]:
        """
        Читает строку.
        
        Args:
            prompt: Текст приглашения для ввода
            required: Обязательно ли поле
            
        Returns:
            Введённая строка или None, если поле не обязательное и пустое
        """
        while True:
            raw = input(prompt).strip()
            if raw == "" and required:
                print("Ошибка: поле не может быть пустым.")
                continue
            return raw if raw else None


class FlatManager:
    """Менеджер для работы с квартирами."""
    
    def __init__(self, storage: Any) -> None:
        """
        Инициализация менеджера.
        
        Args:
            storage: Объект хранилища (MemoryStorage, JSONStorage или CSVStorage)
        """
        self.validator = InputValidator()
        self.storage = storage
    
    def add_flat(self) -> None:
        """Добавление новой записи о квартире."""
        print("\nДобавление записи")
        flat_id = self.validator.read_int("id: ")
        rooms_amount = self.validator.read_int("rooms_amount: ")
        street = input("street: ").strip()
        house_number = self.validator.read_int("house_number: ")
        square = self.validator.read_float("square: ")
        cost = self.validator.read_float("cost: ")
        
        try:
            record = self.storage.create_record(
                flat_id, rooms_amount, street, house_number, square, cost
            )
            print(f"Запись добавлена: {record}")
        except Exception as exc:
            print(f"Ошибка: {exc}")
    
    def show_all(self) -> None:
        """Показать все записи."""
        print("\nСписок записей")
        records = self.storage.select_record()
        self._print_records(records)
    
    def find_flat(self) -> None:
        """Поиск записей по фильтру."""
        print("\nПоиск по фильтру (Enter = пропустить поле)")
        flat_id = self.validator.read_opt_int("id: ")
        rooms_amount = self.validator.read_opt_int("rooms_amount: ")
        street = input("street: ").strip() or None
        house_number = self.validator.read_opt_int("house_number: ")
        square = self.validator.read_opt_float("square: ")
        cost = self.validator.read_opt_float("cost: ")
        
        records = self.storage.select_record(
            flat_id=flat_id,
            rooms_amount=rooms_amount,
            street=street,
            house_number=house_number,
            square=square,
            cost=cost
        )
        self._print_records(records)
    
    def update_flat(self) -> None:
        """Обновление существующей записи."""
        print("\nОбновление записи (Enter = оставить без изменений)")
        flat_id = self.validator.read_int("id записи для обновления: ")
        
        # Проверяем, существует ли запись
        existing = self.storage.select_record(flat_id=flat_id)
        if not existing:
            print(f"Запись с ID {flat_id} не найдена")
            return
        
        print("Введите новые значения (Enter = пропустить):")
        rooms_amount = self.validator.read_opt_int("rooms_amount: ")
        street = input("street: ").strip() or None
        house_number = self.validator.read_opt_int("house_number: ")
        square = self.validator.read_opt_float("square: ")
        cost = self.validator.read_opt_float("cost: ")
        
        try:
            updated = self.storage.update_record(
                flat_id=flat_id,
                rooms_amount=rooms_amount,
                street=street,
                house_number=house_number,
                square=square,
                cost=cost,
            )
            print(f"Запись обновлена: {updated}")
        except Exception as exc:
            print(f"Ошибка: {exc}")
    
    def delete_flat(self) -> None:
        """Удаление записи."""
        print("\nУдаление записи")
        flat_id = self.validator.read_int("id записи для удаления: ")
        
        # Проверяем, существует ли запись
        existing = self.storage.select_record(flat_id=flat_id)
        if not existing:
            print(f"Запись с ID {flat_id} не найдена")
            return
        
        confirm = input("Подтвердите удаление (y/n): ").strip().lower()
        if confirm == 'y':
            try:
                deleted = self.storage.delete_record(flat_id)
                print(f"Запись удалена: {deleted}")
            except Exception as exc:
                print(f"Ошибка: {exc}")
        else:
            print("Удаление отменено")
    
    def _print_records(self, records: list) -> None:
        """
        Выводит список записей.
        
        Args:
            records: Список записей для вывода
        """
        if not records:
            print("Записи не найдены")
            return
        
        for record in records:
            print(record)


class Application:
    """Главный класс приложения."""
    
    def __init__(self, storage: Any) -> None:
        """
        Инициализация приложения.
        
        Args:
            storage: Объект хранилища (MemoryStorage, JSONStorage или CSVStorage)
        """
        self.menu_printer = MenuPrinter()
        self.flat_manager = FlatManager(storage)
        self.actions = {
            "1": self.flat_manager.add_flat,
            "2": self.flat_manager.show_all,
            "3": self.flat_manager.find_flat,
            "4": self.flat_manager.update_flat,
            "5": self.flat_manager.delete_flat,
        }
    
    def run(self) -> None:
        """Запуск основного цикла приложения."""
        while True:
            self.menu_printer.print_menu()
            choice = input("Выберите действие: ").strip()
            
            if choice == "0":
                print("Выход из программы.")
                break
            
            if choice in self.actions:
                self.actions[choice]()
            else:
                print("Неизвестная команда. Повторите ввод.")


def run(storage: Any = None) -> None:
    """
    Запуск TUI приложения.
    
    Args:
        storage: Объект хранилища (если None, будет использовано in-memory)
    """
    if storage is None:
        from src.db.backend.memoryLAB2 import FlatTable
        storage = FlatTable()
    
    app = Application(storage)
    app.run()


if __name__ == "__main__":
    from src.db.backend.memoryLAB2 import FlatTable
    storage = FlatTable()
    app = Application(storage)
    app.run()