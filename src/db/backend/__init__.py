from src.db.backend.memory import FlatTable
from src.db.backend.json_storage import JSONStorage
from src.db.backend.csv_storage import CSVStorage
from src.db.backend.errors import InvalidRoomsAmountError,InvalidHouseNumberError,InvalidSquareError,InvalidCostError,DuplicateIDError,DatabaseError,TableNotFoundError,TableAlreadyExistsError,InvalidStorageDataError,MissingColumnError,UnknownColumnError

def create_storage(storage_type: str = "memory", data_dir: str = "data"):
    if storage_type == "memory":
        return FlatTable()
    elif storage_type == "json":
        return JSONStorage(data_dir)
    elif storage_type == "csv":
        return CSVStorage(data_dir)
    else:
        raise ValueError(f"Неизвестный тип хранилища: {storage_type}")