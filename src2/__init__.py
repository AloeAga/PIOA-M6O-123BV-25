from src1.db1.backend1.memoryLAB3 import FlatTable
from src2.json_storage import JSONStorage
from src2.csv_storage import CSVStorage
from src2.errorsLAB4 import *

def create_storage(storage_type: str = "memory", data_dir: str = "data"):
    if storage_type == "memory":
        return FlatTable()
    elif storage_type == "json":
        return JSONStorage(data_dir)
    elif storage_type == "csv":
        return CSVStorage(data_dir)
    else:
        raise ValueError(f"Неизвестный тип хранилища: {storage_type}")