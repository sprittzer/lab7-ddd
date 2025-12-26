from uuid import UUID
from domain.entities import Order
from .interfaces import OrderRepository, PaymentGateway

class PayOrderUseCase:
    def __init__(self, repo: OrderRepository, gateway: PaymentGateway) -> None:
        self.repo: OrderRepository = repo
        self.gateway: PaymentGateway = gateway
    
    def execute(self, order_id: UUID) -> bool:
        order: Order = self.repo.get_by_id(order_id)
        order.pay()
        
        success: bool = self.gateway.charge(order_id, order.total)
        if success:
            self.repo.save(order)
        return success
