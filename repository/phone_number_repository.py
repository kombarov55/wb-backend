from sqlalchemy.orm import Session

from config import database
from model.phone_number import PhoneNumberVO


def save(session: Session, vo: PhoneNumberVO):
    session.add(vo)
    session.commit()
    session.refresh(vo)
    return vo


def get_all(session: Session):
    return session.query(PhoneNumberVO).all()


def count_activated():
    with database.engine.connect() as con:
        rows = con.execute("select count(*) from phone_number where status = 'ACTIVATED'")
        result = []
        for row in rows:
            result.append(row[0])
        if len(result) == 0:
            return None
        else:
            return result[0]
