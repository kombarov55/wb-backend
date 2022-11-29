import json
from datetime import datetime

from config import database
from model.task_request import TaskRequestVO, TaskRequestStatus


def process(body):
    task_request = to_vo(body)

    session = database.session_local()
    print("saving:")
    print(task_request)
    session.add(task_request)
    session.commit()
    session.close()


def to_vo(body: dict):
    return TaskRequestVO(
        article_select_type=body["article_select_type"],
        article_select_value=body["article_select_value"],
        received_datetime=datetime.now(),
        status=TaskRequestStatus.not_started,
        action_type=body["action_type"],
        params_json=json.dumps(body["params"]),
        amount=body["amount"],
        interval_days=body["interval_days"],
        interval_hours=body["interval_hours"],
        interval_minutes=body["interval_minutes"],
        interval_seconds=body["interval_seconds"]
    )
