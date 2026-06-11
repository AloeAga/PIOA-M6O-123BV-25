# src/db/backend/errors.py
class FlatTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей Flat."""
    pass

class InvalidRoomsAmountError(FlatTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным кол-вом комнат."""
    pass

class InvalidHouseNumberError(FlatTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным номером дома."""
    pass

class InvalidSquareError(FlatTableError):
    """Ошибка, возникающая при попытке создать запись с некорректной площадью."""
    pass

class InvalidCostError(FlatTableError):
    """Ошибка, возникающая при попытке создать запись с некорректной стоимостью."""
    pass

class DuplicateIDError(FlatTableError):
    """Ошибка, возникающая при попытке создать запись с уже существующим идентификатором."""
    pass