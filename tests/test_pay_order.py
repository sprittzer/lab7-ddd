import pytest
from uuid import uuid4
from decimal import Decimal
from domain.entities import Order
from domain.value_objects import Money
from application.use_cases import PayOrderUseCase
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway

def test_successful_payment(use_case: PayOrderUseCase, repo: InMemoryOrderRepository) -> None:
    order_id = uuid4()
    order = Order(order_id)
    order.add_line(uuid4(), 2, Money(Decimal('100')))
    repo.save(order)
    
    result = use_case.execute(order_id)
    
    assert result is True
    saved_order = repo.get_by_id(order_id)
    assert saved_order.status.value == "paid"
    assert saved_order.total.amount == Decimal('200')

def test_empty_order(use_case: PayOrderUseCase, repo: InMemoryOrderRepository) -> None:
    order_id = uuid4()
    order = Order(order_id)
    repo.save(order)
    
    with pytest.raises(ValueError, match="Cannot pay empty order"):
        use_case.execute(order_id)

def test_already_paid(use_case: PayOrderUseCase, repo: InMemoryOrderRepository) -> None:
    order_id = uuid4()
    order = Order(order_id)
    order.add_line(uuid4(), 1, Money(Decimal('100')))
    order.pay()
    repo.save(order)
    
    with pytest.raises(ValueError, match="Order already paid"):
        use_case.execute(order_id)

def test_cannot_modify_after_payment(use_case: PayOrderUseCase, repo: InMemoryOrderRepository) -> None:
    order_id = uuid4()
    order = Order(order_id)
    order.add_line(uuid4(), 1, Money(Decimal('100')))
    repo.save(order)
    
    use_case.execute(order_id)
    saved_order = repo.get_by_id(order_id)
    
    with pytest.raises(ValueError, match="Cannot modify paid order"):
        saved_order.add_line(uuid4(), 1, Money(Decimal('50')))

def test_total_calculation(use_case: PayOrderUseCase, repo: InMemoryOrderRepository) -> None:
    order_id = uuid4()
    order = Order(order_id)
    order.add_line(uuid4(), 2, Money(Decimal('100')))
    order.add_line(uuid4(), 1, Money(Decimal('150')))
    repo.save(order)
    
    assert order.total.amount == Decimal('350')
