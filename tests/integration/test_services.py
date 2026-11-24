import pytest

from src.exceptions import OrderNotFoundError, OutOfStockError
from src.models import DeviceStatus
from src.services import InventoryService, OrderService


def test_full_repair_lifecycle_and_loyalty_discount(db_session):
    inventory = InventoryService(db_session)
    orders = OrderService(db_session)

    inventory.register_or_restock_part(
        sku="BAT-IP13", name="Аккумулятор iPhone 13", price=80.0, quantity=5
    )

    order1 = orders.create_order(
        client_name="Иван Петров",
        client_phone="+3751112233",
        device_type="смартфон",
        brand="Apple",
        problem_description="быстро разряжается",
        initial_labor_cost=40.0,
    )

    orders.add_part_to_order(order_id=order1.id, part_sku="BAT-IP13", quantity=1)
    assert order1.device.status == DeviceStatus.IN_PROGRESS

    orders.complete_order(order_id=order1.id)
    assert order1.calculate_total_cost() == 120.0
    assert inventory.get_part_by_sku("BAT-IP13").stock_quantity == 4

    order2 = orders.create_order(
        client_name="Иван Петров",
        client_phone="+3751112233",
        device_type="ноутбук",
        brand="Lenovo",
        problem_description="чистка от пыли",
        initial_labor_cost=100.0,
    )
    orders.complete_order(order_id=order2.id)

    assert order2.client.id == order1.client.id
    assert order2.client.discount_percent == 5.0
    assert order2.calculate_total_cost() == 95.0


def test_add_part_out_of_stock_does_not_corrupt_order(db_session):
    inventory = InventoryService(db_session)
    orders = OrderService(db_session)

    inventory.register_or_restock_part(
        sku="SCR-SAM-S23", name="Экран Samsung S23", price=200.0, quantity=1
    )

    order = orders.create_order(
        client_name="Мария",
        client_phone="+375556677",
        device_type="смартфон",
        brand="Samsung",
        problem_description="трещина",
    )

    with pytest.raises(OutOfStockError):
        orders.add_part_to_order(order_id=order.id, part_sku="SCR-SAM-S23", quantity=3)

    assert inventory.get_part_by_sku("SCR-SAM-S23").stock_quantity == 1
    assert len(order.order_parts) == 0


def test_complete_nonexistent_order_raises_error(db_session):
    orders = OrderService(db_session)
    with pytest.raises(OrderNotFoundError):
        orders.complete_order(order_id=123)
