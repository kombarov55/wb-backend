from sqlalchemy import Column, Integer, String, DateTime

from config import database


class TaskRequestVO(database.base):
    __tablename__ = "task_request"

    id = Column(Integer, primary_key=True, index=True)
    article_select_type = Column(String)
    article_select_value = Column(String)
    status = Column(String)
    received_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    action_type = Column(String)
    params_json = Column(String)
    amount = Column(Integer)
    interval_days = Column(Integer)
    interval_hours = Column(Integer)
    interval_minutes = Column(Integer)
    interval_seconds = Column(Integer)


class ArticleSelectType:
    by_article = "По артикулу"
    by_shop = "По магазину"
    by_search = "По поисковому запросу"


class ActionType:
    add_question = "Задать вопрос"
    look_at_article = "Посмотреть на артикул"
    set_like_to_comment = "Проставить лайк к комменту"


class TaskRequestStatus:
    not_started = "NOT_STARTED"
    started = "STARTED"
    success = "SUCCESS"
