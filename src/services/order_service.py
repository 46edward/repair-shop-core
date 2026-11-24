from sqlalchemy.orm import Session

from src.exceptions import OrderNotFoundError, PartNotFoundError
from src.models import ClientModel, DeviceModel, DeviceStatus, OrderPartModel, RepairOrderModel
from src.repositories import ClientRepository, OrderRepository, PartRepository


class OrderService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.client_repo = ClientRepository(session)
        self.order_repo = OrderRepository(session)
        self.part_repo = PartRepository(session)

    def create_order(
        self,
        client_name: str,
        client_phone: str,
        device_type: str,
        brand: str,
        problem_description: str,
        initial_labor_cost: float = 0.0,
    ) -> RepairOrderModel:
        client = self.client_repo.get_by_phone(client_phone)
        if not client:
            client = ClientModel(full_name=client_name, phone=client_phone)
            self.client_repo.add(client)

        device = DeviceModel(
            device_type=device_type,
            brand=brand,
            problem_description=problem_description,
            status=DeviceStatus.ACCEPTED,
        )
        order = RepairOrderModel(client=client, device=device)
        order.labor_cost = initial_labor_cost

        self.order_repo.add(order)
        self.session.commit()
        return order

    def add_part_to_order(
        self, order_id: int, part_sku: str, quantity: int = 1
    ) -> RepairOrderModel:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f"Заказ {order_id} не найден")

        part = self.part_repo.get_by_sku(part_sku)
        if not part:
            raise PartNotFoundError(f"Запчасть {part_sku} не найдена на складе")

        part.deduct_stock(quantity)

        existing_item = next(
            (item for item in order.order_parts if item.part is part or item.part_ip == part.id),
            None,
        )

        if existing_item:
            existing_item.quantity += quantity

        else:
            order_part = OrderPartModel(
                order=order, part=part, quantity=quantity, unit_price=part.price
            )
            self.session.add(order_part)

        if order.device.status == DeviceStatus.ACCEPTED:
            order.device.update_status(DeviceStatus.IN_PROGRESS)

        self.session.commit()
        return order

    def complete_order(
        self, order_id: int, final_labor_cost: float | None = None
    ) -> RepairOrderModel:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f"Заказ {order_id} не найден")

        if final_labor_cost is not None:
            order.labor_cost = final_labor_cost

        order.device.update_status(DeviceStatus.COMPLETED)

        completed_count = sum(
            1 for o in order.client.orders if o.device.status == DeviceStatus.COMPLETED
        )

        if completed_count >= 5 and order.client.discount_percent < 10.0:
            order.client.discount_percent = 10.0
        elif completed_count >= 2 and order.client.discount_percent < 5.0:
            order.client.discount_percent = 5.0

        self.session.commit()
        return order

    def get_order_summary(self, order_id: int) -> str:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f"Заказ {order_id} не найден")
        return str(order.get_order_info())
