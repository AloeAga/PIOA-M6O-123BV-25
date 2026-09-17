class DatabaseError(Exception):
    """Базовый класс для всех ошибок базы данных."""
    pass
class InvalidRoomsAmountError(DatabaseError):
    """Ошибка: некорректное количество комнат."""
    pass
class InvalidHouseNumberError(DatabaseError):
    """Ошибка: некорректный номер дома."""
    pass
class InvalidSquareError(DatabaseError):
    """Ошибка: некорректная площадь."""
    pass
class InvalidCostError(DatabaseError):
    """Ошибка: некорректная стоимость."""
    pass
class DuplicateIDError(DatabaseError):
    """Ошибка: запись с таким ID уже существует."""
    pass
class TableNotFoundError(DatabaseError):
    """Ошибка при обращении к несуществующей таблице или записи."""
    pass
class TableAlreadyExistsError(DatabaseError):
    """Ошибка при попытке создать уже существующую таблицу."""
    pass
class InvalidStorageDataError(DatabaseError):
    """Ошибка при чтении повреждённых данных из файла."""
    pass
class MissingColumnError(DatabaseError):
    """Ошибка при отсутствии обязательного поля в записи."""
    pass
class UnknownColumnError(DatabaseError):
    """Ошибка при использовании поля, которого нет в схеме."""
    pass
class FlatTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей Flat."""
    pass