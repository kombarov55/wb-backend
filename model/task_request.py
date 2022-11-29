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
    by_article = "Список артикулов через 'ENTER'"
    by_shop = "Найти по магазину"
    by_search = "Найти по поисковому запросу"


class ActionType:
    add_question = "Задать вопрос"
    add_comparison_question = "Задать вопрос со сравнением"
    look_at_article = "Просмотр"
    set_like_to_comment = "Проставить лайк к комменту"
    set_dislike_to_comment = "Проставить дизлайк к комменту"


class TaskRequestStatus:
    not_started = "NOT_STARTED"
    started = "STARTED"
    success = "SUCCESS"
