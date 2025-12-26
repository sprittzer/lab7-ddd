from uuid import uuid4
from decimal import Decimal
from domain.entities import Order
from domain.value_objects import Money
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase

def main() -> None:
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    order_id = uuid4()
    order = Order(order_id)
    order.add_line(uuid4(), 2, Money(Decimal('100')))
    order.add_line(uuid4(), 1, Money(Decimal('150')))
    
    print(f"Заказ {order_id}: {len(order.lines)} строк, сумма {order.total.amount}")
    repo.save(order)
    
    success = use_case.execute(order_id)
    print(f"Оплата {'прошла' if success else 'не прошла'}")
    
    saved_order = repo.get_by_id(order_id)
    print(f"Статус: {saved_order.status.value}")
    print(f"Итого: {saved_order.total.amount}")



if __name__ == "__main__":
    main()
