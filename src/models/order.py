from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.exceptions import InvalidCostError

if TYPE_CHECKING:
    from src.models.client import ClientModel
    from src.models.device import DeviceModel
    from src.models.part import PartModel


class OrderPartModel(Base):
    __tablename__ = "order_parts"

    order_id: Mapped[int] = mapped_column(ForeignKey("repair_orders.id"), primary_key=True)
    part_ip: Mapped[int] = mapped_column(ForeignKey("parts.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Float)

    order: Mapped["RepairOrderModel"] = relationship(back_populates="order_parts")
    part: Mapped["PartModel"] = relationship()


class RepairOrderModel(Base):
    __tablename__ = "repair_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    _labor_cost: Mapped[float] = mapped_column("labor_cost", Float, default=0.0)

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["ClientModel"] = relationship(back_populates="orders")

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    device: Mapped["DeviceModel"] = relationship(back_populates="order")

    order_parts: Mapped[list["OrderPartModel"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    @property
    def labor_cost(self) -> float:
        return self._labor_cost

    @labor_cost.setter
    def labor_cost(self, new_labor_cost: float) -> None:
        if new_labor_cost < 0:
            raise InvalidCostError("Стоимость работ не может быть отрицательной")
        self._labor_cost = new_labor_cost

    def calculate_total_cost(self) -> float:
        """Calculate (labor cost + parts) - discount%"""
        parts_total = sum(item.quantity * item.unit_price for item in self.order_parts)
        subtotal = self._labor_cost + parts_total
        discount = subtotal * (self.client.discount_percent / 100)
        return round(subtotal - discount, 2)

    def get_order_info(self):
        return (
            f"{self.id} | "
            f"{self.client.full_name} | "
            f"{self.device.device_type} {self.device.brand} | "
            f"{self.calculate_total_cost()} | "
            f"{self.device.status.value}"
        )
