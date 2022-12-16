from datetime import datetime

from sqlalchemy.orm import Session

from src.wb_backend.config import database
from src.wb_backend.model.proxy import ProxyVO


def get_all(session: Session, offset: int, limit: int):
    return session.query(ProxyVO).all()


def save(session: Session, x: dict):
    vo = ProxyVO(
        ip=x["ip"],
        username=x["username"],
        password=x["password"],
        created_datetime=datetime.now()
    )

    session.add(vo)
    session.commit()
    session.refresh(vo)
    return vo


def delete(id: int):
    with database.engine.connect() as con:
        con.execute("delete from proxy where id={}".format("id"))
