from sqlalchemy import Column, Integer, String, DateTime

from src.wb_backend.config import database


class ProxyVO(database.base):
    __tablename__ = "proxy"

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    username = Column(String)
    password = Column(String)
    created_datetime = Column(DateTime)
