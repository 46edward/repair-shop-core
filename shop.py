from enum import Enum
from dataclasses import dataclass, field
from sqlalchemy import create_engine, String, Float, Enum as SQLEnum, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

engine = create_engine("sqlite:///repair_shop.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class DeviceStatus(Enum):
    ACCEPTED = "Принят"
    IN_PROGRESS = "В процессе"
    READY = "Готов"
    COMPLETED = "Завершен"

def log_action(func):
    def wrapper(self, *args, **kwargs):
        print(F"Произошел запуск фукции {func.__name__} с аргументами {args}")
        result = func(self, *args, **kwargs)
        print(F"Функция {func.__name__} успешно выполнилась.")
        return result
    return wrapper


class DeviceModel(Base):

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_type: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    problem_description: Mapped[str] = mapped_column(String(256))
    status: Mapped[DeviceStatus] = mapped_column(SQLEnum(DeviceStatus), default=DeviceStatus.ACCEPTED)

    order: Mapped["RepairOrderModel"] = relationship(back_populates="device", uselist=False)

    def __str__(self):
        return (
            f"[{self.device_type}] - "
            f"Проблема: {self.problem_description} "
            f"(Статус: {self.status.value})."
        )
    def update_status(self, new_status: DeviceStatus):
        self.status = new_status


class RepairOrderModel(Base):
    __tablename__ = "repair_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_name: Mapped[str] = mapped_column(String(100))
    _cost: Mapped[float] = mapped_column("cost", Float, default=0.0)

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    device: Mapped[DeviceModel] = relationship(back_populates="order")


    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, new_cost: float) -> None:
        if new_cost < 0:
            raise ValueError("Отрицательныое значение цены")
        self._cost = new_cost


    def get_order_info(self):
        return (
            f"{self.id} | "
            f"{self.client_name} | "
            f"{self.device.device_type} {self.device.brand} | "
            f"{self.cost} | "
            f"{self.device.status.value}"
        )

if __name__ == "__main__":

    Base.metadata.create_all(engine)
    session = SessionLocal()
            
    # 1. Создаем устройство
    my_phone = DeviceModel(device_type="смартфон", brand="Xiaomi", problem_description="разбит экран")

    # 2. Создаем заказ, передавая туда устройство
    order = RepairOrderModel(client_name="Алексей", device=my_phone, _cost=150.0)

    session.add(my_phone)
    session.add(order)
    session.commit()
    print("Заказ сохранен в базу")
    session.close()