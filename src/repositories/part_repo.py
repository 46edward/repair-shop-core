from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models import PartModel

class PartRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, part: PartModel) -> PartModel:
        self.session.add(part)
        self.session.flush()
        return part

    def get_by_sku(self, sku: str) -> PartModel | None:
        stmt = select(PartModel).where(PartModel.sku == sku)
        return self.session.scalar(stmt)

    def list_low_stock(self, threshold: int = 2) -> list[PartModel]:
        stmt = select(PartModel).where(PartModel.stock_quantity <= threshold)
        return list(self.session.scalars(stmt).all())