from sqlalchemy import Column, Integer, String

from src.wb_backend.config import database


class PhoneNumberVO(database.base):
    __tablename__ = "phone_number"

    id = Column(Integer, primary_key=True, index=True)
    ext_id = Column(String)
    number = Column(String)
    cookies_json = Column(String)
    status = Column(String)


class PhoneNumberStatus:
    just_received = "JUST_RECEIVED"
    activating = "ACTIVATING"
    activated = "ACTIVATED"
    blocked = "BLOCKED"