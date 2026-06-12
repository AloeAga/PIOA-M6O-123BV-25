class InvalidRoomsAmountError(Exception):
    """Ошибка: некорректное количество комнат"""
    pass

class InvalidHouseNumberError(Exception):
    """Ошибка: некорректный номер дома"""
    pass

class InvalidSquareError(Exception):
    """Ошибка: некорректная площадь"""
    pass

class InvalidCostError(Exception):
    """Ошибка: некорректная стоимость"""
    pass

class DuplicateIDError(Exception):
    """Ошибка: запись с таким ID уже существует"""
    pass


class DatabaseError(Exception):
    """Базовый класс для ошибок базы данных"""
    pass

class TableNotFoundError(DatabaseError):
    """Ошибка, возникающая при обращении к несуществующей таблице"""
    pass

class TableAlreadyExistsError(DatabaseError):
    """Ошибка, возникающая при попытке создать уже существующую таблицу"""
    pass

class InvalidStorageDataError(DatabaseError):
    """Ошибка, возникающая при чтении повреждённых данных из файла"""
    pass

class MissingColumnError(DatabaseError):
    """Ошибка, возникающая при отсутствии обязательного поля в записи"""
    pass

class UnknownColumnError(DatabaseError):
    """Ошибка, возникающая при использовании поля, которого нет в схеме"""
    pass