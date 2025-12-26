# Лабораторная: Слоистая архитектура + DDD

Реализовала систему оплаты заказа по слоям: Domain, Application, Infrastructure + тесты.

## Структура
```
order_payment/
├── domain/ # Order агрегат + инварианты
├── application/ # PayOrderUseCase
├── infrastructure/ # InMemoryOrderRepository + FakePaymentGateway
└── tests/ # 5 unit-тестов
```


## Domain
- `Order` - агрегат с инвариантами
- `Money` - value object 
- `OrderStatus` - enum (DRAFT/PAID)

**Инварианты в Order.pay():**
- нельзя оплатить пустой заказ
- нельзя оплатить повторно  
- после оплаты нельзя add_line()
- total = sum(line.total)

## Use-case
```python
def execute(self, order_id):
order = repo.get_by_id(order_id) # DIP
order.pay() # Domain
gateway.charge(order_id, order.total) # Infrastructure
repo.save(order)
```

Тесты проверяют все инварианты + успешную оплату.