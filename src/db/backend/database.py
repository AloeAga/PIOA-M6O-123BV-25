from abc import ABC, abstractmethod
from typing import Optional

type FlatRecord = tuple[int, int, str, int, float, float]


class Database(ABC):
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
        """
        Создаёт новую запись.
        
        Args:
            flat_id: Уникальный идентификатор квартиры
            rooms_amount: Количество комнат
            street: Название улицы
            house_number: Номер дома
            square: Площадь в кв.м
            cost: Стоимость в млн.руб
            
        Returns:
            Созданная запись
            
        Raises:
            InvalidRoomsAmountError: Если комнат < 1
            InvalidHouseNumberError: Если номер дома < 1
            InvalidSquareError: Если площадь < 0
            InvalidCostError: Если стоимость < 0
            DuplicateIDError: Если ID уже существует
        """
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
        """
        Выбирает записи по фильтрам.
        
        Returns:
            Список записей, удовлетворяющих фильтрам
        """
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
        """
        Обновляет существующую запись.
        
        Args:
            flat_id: ID записи для обновления
            rooms_amount: Новое количество комнат (None = не менять)
            street: Новая улица (None = не менять)
            house_number: Новый номер дома (None = не менять)
            square: Новая площадь (None = не менять)
            cost: Новая стоимость (None = не менять)
            
        Returns:
            Обновлённая запись
            
        Raises:
            TableNotFoundError: Если запись с указанным ID не найдена
            InvalidRoomsAmountError: Если новое значение комнат < 1
            InvalidHouseNumberError: Если новый номер дома < 1
            InvalidSquareError: Если новая площадь < 0
            InvalidCostError: Если новая стоимость < 0
        """
        pass
    
    @abstractmethod
    def delete_record(self, flat_id: int) -> FlatRecord:
        """
        Удаляет запись по ID.
        
        Args:
            flat_id: ID записи для удаления
            
        Returns:
            Удалённая запись
            
        Raises:
            TableNotFoundError: Если запись с указанным ID не найдена
        """
        pass
    
    # ========== Дополнительные операции ==========
    
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