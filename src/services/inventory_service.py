from sqlalchemy.orm import Session
from src.models import PartModel
from src.repositories import PartRepository
from src.exceptions import PartNotFoundError

class InventoryService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.part_repo = PartRepository(session)

    def register_or_restock_part(
            self,
            sku: str,
            name: str,
            price: float,
            quantity: int,
    ) -> PartModel:
        part = self.part_repo.get_by_sku(sku)
        if part:
            part.restock(quantity)
            part.price = price
        else:
            part = PartModel(
                sku = sku,
                name = name,
                price = price,
                stock_quantity = quantity
                )
            self.part_repo.add(part)
       
        self.session.commit()
        return part

    def get_part_by_sku(self, sku: str) -> PartModel:
        part = self.part_repo.get_by_sku(sku)
        if not part:
            raise PartNotFoundError(f"Запчасть с антикулом {sku} не найдена на складе")
        return part

    def get_low_stock_alerts(self, threshold: int = 2) -> list[PartModel]:
        return self.part_repo.list_low_stock(threshold = threshold)