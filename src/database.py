from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///repair_shop.db"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def init_db() -> None:
    from src.models import DeviceModel, RepairOrderModel
    Base.metadata.create_all(engine)
