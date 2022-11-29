import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

import wb_service
from config import database
from model.task import TaskVO, TaskStatus
from model.task_request import TaskRequestVO, TaskRequestStatus, ArticleSelectType


def process(body):
    print("received:")
    print(body)

    task_request = to_vo(body)

    session = database.session_local()
    save_task_request(session, task_request)

    articles = find_articles(task_request.article_select_type, task_request.article_select_value)

    for article in articles:
        tasks = schedule_tasks(article, task_request)
        for task in tasks:
            session.add(task)
        session.commit()

    session.close()

def save_task_request(session: Session, task_request: TaskRequestVO) -> TaskRequestVO:
    session.add(task_request)
    session.commit()
    return task_request


def find_articles(article_select_type: str, article_select_value: str) -> list[str]:
    if article_select_type == ArticleSelectType.by_article:
        return article_select_value.split("\n")
    if article_select_type == ArticleSelectType.by_shop:
        return wb_service.find_all_artcies_by_shop_id(article_select_value)
    if article_select_type == ArticleSelectType.by_search:
        return wb_service.find_all_articles_by_search_query(article_select_value)


def schedule_tasks(article: str, task_request: TaskRequestVO) -> list[TaskVO]:
    result = []
    now = datetime.now()

    for i in range(0, task_request.amount):
        task = TaskVO(
            task_request_id=task_request.id,
            article=article,
            action_type=task_request.action_type,
            params_json=task_request.params_json,
            scheduled_datetime=now + timedelta(
                days=task_request.interval_days * i,
                hours=task_request.interval_hours * i,
                minutes=task_request.interval_minutes * i,
                seconds=task_request.interval_seconds * i
            ),
            status=TaskStatus.scheduled
        )
        result.append(task)

    return result


def to_vo(body: dict) -> TaskRequestVO:
    return TaskRequestVO(
        article_select_type=body["article_select_type"],
        article_select_value=body["article_select_value"],
        received_datetime=datetime.now(),
        status=TaskRequestStatus.not_started,
        action_type=body["action_type"],
        params_json=json.dumps(body["params"]),
        amount=body["amount"],
        interval_days=body["interval_days"] or 0,
        interval_hours=body["interval_hours"] or 0,
        interval_minutes=body["interval_minutes"] or 0,
        interval_seconds=body["interval_seconds"] or 0
    )
