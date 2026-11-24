import pytest

from src.exceptions import InvalidCostError, OutOfStockError
from src.models import DeviceStatus, OrderPartModel


def test_device_update_status(sample_device):
    sample_device.update_status(DeviceStatus.COMPLETED)
    assert sample_device.status == DeviceStatus.COMPLETED


def test_order_labor_cost_negative_raises_error(sample_order):
    with pytest.raises(InvalidCostError, match="Стоимость работ не может быть отрицательной"):
        sample_order.labor_cost = -10.0


def test_part_deduct_stock_success(sample_part):
    sample_part.deduct_stock(2)
    assert sample_part.stock_quantity == 3


def test_part_deduct_stock_out_of_stock_raises_error(sample_part):
    with pytest.raises(OutOfStockError):
        sample_part.deduct_stock(10)


def test_order_calculate_total_cost_with_parts_and_discount(sample_order, sample_part):
    OrderPartModel(order=sample_order, part=sample_part, quantity=1, unit_price=sample_part.price)

    # Работа: 100.0, Запчасть: 1 шт * 100.0 = 100.0 -> Подытог: 200.0
    # Скидка клиента: 10% -> Итого: 180.0

    assert sample_order.calculate_total_cost() == 180.0
