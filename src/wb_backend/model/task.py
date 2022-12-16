from sqlalchemy import Column, Integer, String, DateTime

from src.wb_backend.config import database


class TaskVO(database.base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    task_request_id = Column(Integer)
    article = Column(String)
    action_type = Column(String)
    params_json = Column(String)
    scheduled_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    number_used = Column(String)
    status = Column(String)


class TaskStatus:
    scheduled = "SCHEDULED"
    running = "RUNNING"
    no_available_numbers = "NO_AVAILABLE_NUMBERS"
    success = "SUCCESS"
    failed = "FAILED"
