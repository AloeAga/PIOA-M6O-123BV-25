from abc import ABC, abstractmethod
from typing import Optional
type FlatRecord = tuple[int, int, str, int, float, float]
class Database(ABC):
    """Абстрактный класс Database с единым интерфейсом для всех хранилищ."""    
    @abstractmethod
    def create_record(
        self,
        flat_id: int,
        rooms_amount: int,
        street: str,
        house_number: int,
        square: float,
        cost: float
    ) -> FlatRecord:
        """Создаёт новую запись."""
        pass   
    @abstractmethod
    def select_record(
        self,
        flat_id: Optional[int] = None,
        rooms_amount: Optional[int] = None,
        street: Optional[str] = None,
        house_number: Optional[int] = None,
        square: Optional[float] = None,
        cost: Optional[float] = None,
    ) -> list[FlatRecord]:
        """Выбирает записи по фильтрам."""
        pass   
    @abstractmethod
    def update_record(
        self,
        flat_id: int,
        rooms_amount: Optional[int] = None,
        street: Optional[str] = None,
        house_number: Optional[int] = None,
        square: Optional[float] = None,
        cost: Optional[float] = None,
    ) -> FlatRecord:
        """Обновляет существующую запись."""
        pass    
    @abstractmethod
    def delete_record(self, flat_id: int) -> FlatRecord:
        """Удаляет запись по ID."""
        pass    
    @abstractmethod
    def clear(self) -> None:
        """Очищает все записи."""
        pass   
    @abstractmethod
    def get_all(self) -> list[FlatRecord]:
        """Возвращает копию всех записей."""
        pass   
    @abstractmethod
    def __len__(self) -> int:
        """Возвращает количество записей."""
        pass