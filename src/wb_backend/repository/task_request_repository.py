from src.wb_backend.config import database


def get_all():
    sql = """
    select tr.id,
       tr.article_select_type,
       tr.article_select_value,
       tr.status,
       tr.received_datetime,
       tr.end_datetime,
       tr.action_type,
       tr.amount,
       tr.interval_days,
       tr.interval_hours,
       tr.interval_minutes,
       tr.interval_seconds,
       (select count(*)
        from task t
        where t.task_request_id = tr.id) total_cnt,
       (select count(*)
        from task t
        where t.task_request_id = tr.id and t.status = 'SUCCESS') success_cnt,
       (select count(*)
        from task t
        where t.task_request_id = tr.id and t.status = 'RUNNING') running_cnt,
       (select count(*)
        from task t
        where t.task_request_id = tr.id and t.status in ('NO_AVAILABLE_NUMBERS', 'FAILED')) no_available_numbers_cnt,
       (select count(*)
        from task t
        where t.task_request_id = tr.id and t.status = 'RUNNING') running_cnt,
       (select count(*)
        from task t
        where t.task_request_id = tr.id and t.status = 'SCHEDULED') scheduled_cnt
    from task_request tr
    order by tr.received_datetime desc
    """

    with database.engine.connect() as con:
        rows = con.execute(sql)
        result = []
        for row in rows:
            result.append(row._asdict())
        return result

