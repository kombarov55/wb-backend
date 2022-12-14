from sqlalchemy.orm import Session

from model.phone_number import PhoneNumberVO


def save(session: Session, vo: PhoneNumberVO):
    session.add(vo)
    session.commit()
    session.refresh(vo)
    return vo


def get_all(session: Session):
    return session.query(PhoneNumberVO).all()
