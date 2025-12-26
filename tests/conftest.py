import pytest
from uuid import uuid4
from domain.entities import Order
from domain.value_objects import Money
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase

@pytest.fixture
def repo() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()

@pytest.fixture
def gateway() -> FakePaymentGateway:
    return FakePaymentGateway()

@pytest.fixture
def use_case(repo: InMemoryOrderRepository, gateway: FakePaymentGateway) -> PayOrderUseCase:
    return PayOrderUseCase(repo, gateway)
