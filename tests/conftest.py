import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.models import DeviceModel, DeviceStatus, RepairOrderModel

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