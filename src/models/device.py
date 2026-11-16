from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if TYPE_CHECKING:
    from src.models.order import RepairOrderModel

class DeviceStatus(Enum):
    ACCEPTED = "Принят"
    IN_PROGRESS = "В процессе"
    READY = "Готов"
    COMPLETED = "Завершен"

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
