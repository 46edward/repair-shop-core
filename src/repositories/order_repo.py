from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models import RepairOrderModel, DeviceModel, DeviceStatus

class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, order: RepairOrderModel) -> RepairOrderModel:
        self.session.add(order)
        self.session.flush()
        return order

    def get_by_id(self, order_id: int) -> RepairOrderModel | None:
        return self.session.get(RepairOrderModel, order_id)

    def list_by_status(self, status: DeviceStatus) -> list[RepairOrderModel]:
        stmt = (
            select(RepairOrderModel)
            .join(RepairOrderModel.device)
            .where(DeviceModel.status == status)
            .order_by(RepairOrderModel.id)
        )
        return list(self.session.scalars(stmt).all())

    def list_all(self) -> list[RepairOrderModel]:
        stmt = select(RepairOrderModel).order_by(RepairOrderModel.id)
        return list(self.session.scalars(stmt).all())