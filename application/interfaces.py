from abc import ABC, abstractmethod
from uuid import UUID
from domain.value_objects import Money
from domain.entities import Order

class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order:
        ...
    
    @abstractmethod
    def save(self, order: Order) -> None:
        ...

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, order_id: UUID, amount: Money) -> bool:
        ...
