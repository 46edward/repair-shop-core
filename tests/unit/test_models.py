import pytest 
from src.models import DeviceStatus
from src.exceptions import InvalidCostError

def test_device_update_status(sample_device):
    sample_device.update_status(DeviceStatus.COMPLETED)
    assert  sample_device.status == DeviceStatus.COMPLETED

def test_order_cost_setter_valid(sample_order):
    sample_order.cost = 150
    assert sample_order.cost == 150

def test_order_cost_setter_negative_raises_error(sample_order):
    with pytest.raises(InvalidCostError, match="Отрицательныое значение цены"):
        sample_order.cost = -100
