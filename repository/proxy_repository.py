from datetime import datetime

from sqlalchemy.orm import Session

from model.proxy import ProxyVO


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
