from typing import List
from uuid import UUID, uuid4
from decimal import Decimal
from .value_objects import Money
from .enums import OrderStatus


class OrderLine:
    def __init__(self, product_id: UUID, quantity: int, unit_price: Money):
        self.product_id: UUID = product_id
        self.quantity: int = quantity
        self.unit_price: Money = unit_price
        self.total: Decimal = unit_price.amount * quantity


class Order:
    def __init__(self, order_id: UUID = None):
        self.id: UUID = order_id or uuid4()
        self._lines: List[OrderLine] = []
        self._status: OrderStatus = OrderStatus.DRAFT
        self._total: Money = Money(Decimal(0))
    
    @property
    def lines(self) -> List[OrderLine]:
        return self._lines
    
    @property
    def status(self) -> OrderStatus:
        return self._status
    
    @property
    def total(self) -> Money:
        return self._total
    
    def add_line(self, product_id: UUID, quantity: int, unit_price: Money) -> None:
        if self._status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        line = OrderLine(product_id, quantity, unit_price)
        self._lines.append(line)
        self._recalculate_total()
    
    def pay(self) -> None:
        if not self._lines:
            raise ValueError("Cannot pay empty order")
        if self._status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        self._status = OrderStatus.PAID
    
    def _recalculate_total(self) -> None:
        total = sum(line.total for line in self._lines)
        self._total = Money(Decimal(total))
