from uuid import UUID
from domain.value_objects import Money

class FakePaymentGateway:
    def charge(self, order_id: UUID, amount: Money) -> bool:
        print(f"Charging {amount.amount} for order {order_id}")
        return True
