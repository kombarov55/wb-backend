from sqlalchemy import Column, Integer, String, DateTime

from src.wb_backend.config import database


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
    set_like_to_comment = "Проставить лайки к комменту"
    set_dislike_to_comment = "Проставить дизлайки к комменту"
    add_to_cart = "Добавить в корзину"
    add_to_cart_and_remove = "Добавить и убрать из корзины"
    remove_from_cart = "Убрать из корзины"
    add_to_favorites = "Добавить в избранное"
    add_to_favorites_and_remove = "Добавить и убрать из избранного"
    remove_from_favorites = "Убрать из избранного"


class TaskRequestStatus:
    not_started = "NOT_STARTED"
    started = "STARTED"
    success = "SUCCESS"
