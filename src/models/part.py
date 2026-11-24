from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.exceptions import OutOfStockError


class PartModel(Base):
    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(
        String(50), unique=True, index=True
    )  # номер артикула запчасти уникальный
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)

    def deduct_stock(self, quantity) -> None:
        """Списывает делати со склада и проверяет остаток"""
        if quantity <= 0:
            raise ValueError("Количество деталей для списания должно быть больше нуля.")
        if self.stock_quantity < quantity:
            raise OutOfStockError(
                f"Недостаточно {self.name} (арт. {self.sku}): "
                f"запрошено {quantity}, на складе {self.stock_quantity}"
            )
        self.stock_quantity -= quantity

    def restock(self, quantity):
        """Пополняет склад новыми делалями"""
        if quantity <= 0:
            raise ValueError("Количество делатей для пополнения должно быть больше нуля.")
        self.stock_quantity += quantity
