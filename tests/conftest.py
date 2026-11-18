import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.models import DeviceModel, DeviceStatus, RepairOrderModel, ClientModel, PartModel

@pytest.fixture
def db_session():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestSessionLocal = sessionmaker(bind=test_engine)
    
    Base.metadata.create_all(test_engine)
    session = TestSessionLocal()
    yield session
    session.close()

@pytest.fixture
def sample_client():
    return ClientModel(
        full_name = "Max",
        phone = "+48090080070",
        discount_percent = 10.0
    )

@pytest.fixture
def sample_device():
    return DeviceModel(
        device_type="смартфон",
        brand="Xiaomi",
        problem_description="разбит экран",
        status=DeviceStatus.ACCEPTED
    )

@pytest.fixture
def sample_part():
    return PartModel(
        sku="AB040312", 
        name="Дисплей Xiaomi 12", 
        price=100.0, 
        stock_quantity=5
    )

@pytest.fixture
def sample_order(sample_device,sample_client):
    return RepairOrderModel(
        client=sample_client,
        device=sample_device,
        _labor_cost=100.0
    )