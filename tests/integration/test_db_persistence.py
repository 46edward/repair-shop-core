from src.models import (
    ClientModel,
    DeviceModel,
    DeviceStatus,
    OrderPartModel,
    PartModel,
    RepairOrderModel,
)


def test_full_order_with_parts_persistance(db_session):
    client = ClientModel(full_name="Max", phone="+48080090080", discount_percent=0.0)
    laptop = DeviceModel(device_type="ноутбук", brand="Apple", problem_description="замена АКБ")
    battery = PartModel(sku="BAT0908412", name="Аккумулятор", price=150.0, stock_quantity=3)

    battery.deduct_stock(1)
    order = RepairOrderModel(client=client, device=laptop, _labor_cost=50.0)
    order.order_parts.append(
        OrderPartModel(order=order, part=battery, quantity=1, unit_price=battery.price)
    )

    db_session.add_all([client, laptop, battery, order])
    db_session.commit()

    saved_order = db_session.query(RepairOrderModel).first()
    assert saved_order is not None
    assert saved_order.client.full_name == "Max"
    assert saved_order.device.status == DeviceStatus.ACCEPTED
    assert saved_order.calculate_total_cost() == 200.0
    assert saved_order.order_parts[0].part.stock_quantity == 2
