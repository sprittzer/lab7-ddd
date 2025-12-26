from typing import Dict
from uuid import UUID
from domain.entities import Order

class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: Dict[UUID, Order] = {}
    
    def get_by_id(self, order_id: UUID) -> Order:
        order: Order = self._orders.get(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        return order
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = order
