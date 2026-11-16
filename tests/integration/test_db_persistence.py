from src.models import DeviceStatus, DeviceModel, RepairOrderModel

def test_save_and_read_order_in_db(db_session):
    device = DeviceModel(device_type="ноутбук", brand="Dell", problem_description="Battery replace")
    order = RepairOrderModel(client_name="Alex", _cost=200, device=device)

    db_session.add(device)
    db_session.add(order)
    db_session.commit()

    assert device.id == 1
    assert order.id == 1
    assert device.status == DeviceStatus.ACCEPTED

    saved_order = db_session.query(RepairOrderModel).filter_by(client_name="Alex").first()

    assert saved_order is not None
    assert saved_order.cost == 200
    assert saved_order.device.brand == "Dell"

    assert "1 | Alex | ноутбук Dell | 200.0 | Принят" == saved_order.get_order_info()

def test_update_status_and_persist_in_db(db_session):
    device = DeviceModel(device_type="phone", brand="Apple", problem_description="Screen replace")
    order = RepairOrderModel(client_name="Jan", _cost=50, device=device)

    db_session.add_all([device, order])
    db_session.commit()

    device.update_status(DeviceStatus.READY)
    db_session.commit()

    updated_order = db_session.query(RepairOrderModel).filter_by(id=order.id).first()
    assert updated_order.device.status == DeviceStatus.READY