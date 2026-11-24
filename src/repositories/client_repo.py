from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import ClientModel


class ClientRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, client: ClientModel) -> ClientModel:
        self.session.add(client)
        self.session.flush()  # get id from DB betore DB commit
        return client

    def get_by_id(self, client_id: int) -> ClientModel | None:
        return self.session.get(ClientModel, client_id)

    def get_by_phone(self, phone: str) -> ClientModel | None:
        stmt = select(ClientModel).where(ClientModel.phone == phone)
        return self.session.scalar(stmt)

    def list_all(self) -> list[ClientModel]:
        stmt = select(ClientModel).order_by(ClientModel.id)
        return list(self.session.scalars(stmt).all())
