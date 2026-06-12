from src2.database import Database
from src2.errorsLAB4 import TableNotFoundError
from src2.table import Table


class MemoryDatabase(Database):
    """База данных, хранящая таблицы в оперативной памяти."""

    def __init__(self) -> None:
        self.tables: dict[str, Table] = {}

    def _table_exists(self, table_name: str) -> bool:
        return table_name in self.tables

    def _load_table(self, table_name: str) -> Table:
        if table_name not in self.tables:
            raise TableNotFoundError(
                f"Таблица '{table_name}' не существует."
            )

        return self.tables[table_name]

    def _save_table(self, table_name: str, table: Table) -> None:
        self.tables[table_name] = table