from typing import TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.exceptions import InvalidCostError

if TYPE_CHECKING:
    from src.models.device import DeviceModel



class RepairOrderModel(Base):
    __tablename__ = "repair_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_name: Mapped[str] = mapped_column(String(100))
    _cost: Mapped[float] = mapped_column("cost", Float, default=0.0)

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    device: Mapped["DeviceModel"] = relationship(back_populates="order")


    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, new_cost: float) -> None:
        if new_cost < 0:
            raise InvalidCostError("Отрицательныое значение цены")
        self._cost = new_cost


    def get_order_info(self):
        return (
            f"{self.id} | "
            f"{self.client_name} | "
            f"{self.device.device_type} {self.device.brand} | "
            f"{self.cost} | "
            f"{self.device.status.value}"
        )