from sqlalchemy import Column, Integer, String, DateTime

from config import database


class PhoneNumberVO(database.base):
    __tablename__ = "phone_number"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String)
    status = Column(String)


class PhoneNumberStatus:
    just_received = "JUST_RECEIVED"
    activated = "ACTIVATED"
    blocked = "BLOCKED"
