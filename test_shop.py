import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shop import Base, DeviceModel, DeviceStatus, RepairOrderModel

@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestSessionLocal = sessionmaker(bind=test_engine)
    
    Base.metadata.create_all(test_engine)
    session = TestSessionLocal()
    yield session
    session.close()

@pytest.fixture
def sample_device():
    return DeviceModel(
        device_type="смартфон",
        brand="Xiaomi",
        problem_description="разбит экран",
        status=DeviceStatus.ACCEPTED
    )

@pytest.fixture
def sample_order(sample_device):
    return RepairOrderModel(
        client_name="Алексей",
        device=sample_device,
        _cost=150.0
    )

def test_device_update_status(sample_device):
    sample_device.update_status(DeviceStatus.COMPLETED)
    assert  sample_device.status == DeviceStatus.COMPLETED

def test_order_cost_setter_valid(sample_order):
    sample_order.cost = 150
    assert sample_order.cost == 150

def test_order_cost_setter_negative_raises_error(sample_order):
    with pytest.raises(ValueError, match="Отрицательныое значение цены"):
        sample_order.cost = -100

def test_get_order_info_formatting(sample_order):
    order =  sample_order.get_order_info() 
    assert "Алексей | смартфон Xiaomi | 150.0 | Принят" in order


def test_save_and_read_order_in_db(db_session):
    device = DeviceModel(device_type="ноутбук", brand="Dell", problem_description="Battery replace")
    order = RepairOrderModel(client_name="Alex", _cost=200, device=device)

    db_session.add(device)
    db_session.add(order)
    db_session.commit()

    assert device.id == 1
    assert order.id == 1
    assert device.status == DeviceStatus.ACCEPTED

    saved_order = db_session.query(RepairOrderModel).filter_by(client_name="Alex").first()

    assert saved_order is not None
    assert saved_order.cost == 200
    assert saved_order.device.brand == "Dell"

    assert "1 | Alex | ноутбук Dell | 200.0 | Принят" == saved_order.get_order_info()

def test_update_status_and_persist_in_db(db_session):
    device = DeviceModel(device_type="phone", brand="Apple", problem_description="Screen replace")
    order = RepairOrderModel(client_name="Edward", _cost=50, device=device)

    db_session.add_all([device, order])
    db_session.commit()

    device.update_status(DeviceStatus.READY)
    db_session.commit()

    updated_order = db_session.query(RepairOrderModel).filter_by(id=order.id).first()
    assert updated_order.device.status == DeviceStatus.READY



    