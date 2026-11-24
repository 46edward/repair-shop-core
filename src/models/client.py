from typing import TYPE_CHECKING

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from order import RepairOrderModel


class ClientModel(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    discount_percent: Mapped[float] = mapped_column(Float, default=0.0)

    orders: Mapped[list["RepairOrderModel"]] = relationship(back_populates="client")

    def __str__(self) -> str:
        return f"{self.full_name} ({self.phone}) - discount {self.discount_percent}%"
