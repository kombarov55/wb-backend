import json
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

import wb_service
from config import database
from model.task import TaskVO, TaskStatus
from model.task_request import TaskRequestVO, TaskRequestStatus, ArticleSelectType, ActionType


def process(body):
    print("received:")
    print(body)

    task_request = to_vo(body)

    session = database.session_local()
    save_task_request(session, task_request)

    articles = find_articles(task_request.article_select_type, task_request.article_select_value)

    if task_request.action_type == ActionType.add_to_cart \
            or task_request.action_type == ActionType.add_to_favorites:
        for i in range(0, len(articles)):
            article = articles[i]
            task = create_task(task_request, article, i)
            session.add(task)
    elif task_request.action_type == ActionType.add_to_cart_and_remove:
        tasks = schedule_add_and_remove_from_cart(task_request, articles)
        for task in tasks:
            session.add(task)
    elif task_request.action_type == ActionType.add_to_favorites_and_remove:
        tasks = schedule_add_and_remove_from_favorites(task_request, articles)
        for task in tasks:
            session.add(task)
    else:
        for article in articles:
            tasks = schedule_tasks(article, task_request)
            for task in tasks:
                session.add(task)

    session.commit()
    session.close()


def save_task_request(session: Session, task_request: TaskRequestVO):
    session.add(task_request)
    session.commit()
    session.refresh(task_request)
    return task_request


def find_articles(article_select_type: str, article_select_value: str):
    if article_select_type == ArticleSelectType.by_article:
        return article_select_value.split("\n")
    if article_select_type == ArticleSelectType.by_shop:
        xs = wb_service.find_items_by_shop_id(article_select_value)
        return list(map(lambda x: x["article"], xs))
    if article_select_type == ArticleSelectType.by_search:
        xs = wb_service.find_items_by_search_query(article_select_value)
        return list(map(lambda x: x["article"], xs))


def schedule_tasks(article: str, task_request: TaskRequestVO):
    result = []

    for i in range(0, task_request.amount):
        task = TaskVO(
            task_request_id=task_request.id,
            article=article,
            action_type=task_request.action_type,
            params_json=task_request.params_json,
            scheduled_datetime=get_random_datetime_in_interval(task_request),
            status=TaskStatus.scheduled
        )
        result.append(task)

    return result


def to_vo(body: dict):
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


def default_schedule(task_request: TaskRequestVO, article: str):
    result = []

    for i in range(0, task_request.amount):
        task = create_task(task_request, article, i)

        result.append(task)

    return result


def schedule_add_and_remove_from_cart(task_request: TaskRequestVO, articles: list):
    result = []

    for article_i in range(0, len(articles)):
        article = articles[article_i]
        for rq_amount_i in range(0, task_request.amount):
            task_add = create_task(task_request, article, article_i + rq_amount_i)
            task_add.action_type = ActionType.add_to_cart
            result.append(task_add)

            task_remove = create_task(task_request, article, rq_amount_i)
            task_remove.action_type = ActionType.remove_from_cart

            params = json.loads(task_request.params_json)

            task_remove.scheduled_datetime = task_add.scheduled_datetime + timedelta(
                days=int(params["remove_interval_days"]),
                hours=int(params["remove_interval_hours"]),
                minutes=int(params["remove_interval_minutes"]),
                seconds=int(params["remove_interval_seconds"])
            )
            result.append(task_remove)

    return result


def schedule_add_and_remove_from_favorites(task_request: TaskRequestVO, articles: list):
    result = []

    for article_i in range(0, len(articles)):
        article = articles[article_i]
        for rq_i in range(0, task_request.amount):
            task_add = create_task(task_request, article, article_i + rq_i)
            task_add.action_type = ActionType.add_to_favorites

            result.append(task_add)

            task_remove = create_task(task_request, article, rq_i)
            task_remove.action_type = ActionType.remove_from_favorites

            params = json.loads(task_request.params_json)

            task_remove.scheduled_datetime = task_add.scheduled_datetime + timedelta(
                days=int(params["remove_interval_days"]),
                hours=int(params["remove_interval_hours"]),
                minutes=int(params["remove_interval_minutes"]),
                seconds=int(params["remove_interval_seconds"])
            )
            result.append(task_remove)

    return result


def create_task(task_request: TaskRequestVO, article: str, i):
    now = datetime.now()

    return TaskVO(
        task_request_id=task_request.id,
        article=article,
        action_type=task_request.action_type,
        params_json=task_request.params_json,
        scheduled_datetime=get_random_datetime_in_interval(task_request),
        status=TaskStatus.scheduled
    )


def get_random_datetime_in_interval(task_request: TaskRequestVO):
    now = datetime.now()
    interval_seconds = task_request.interval_days * 60 * 60 * 24 \
                       + task_request.interval_hours * 60 * 60 \
                       + task_request.interval_minutes * 60 \
                       + task_request.interval_seconds

    seconds_to_add = random.randint(0, interval_seconds)
    return now + timedelta(seconds=seconds_to_add)
