from config import database


def find_by_task_request_id(id: int):
    sql = """
    select id, 
    article, 
    action_type, 
    scheduled_datetime, 
    end_datetime, 
    number_used, 
    error_msg,
    status
    from task
    where task_request_id = {} 
    order by scheduled_datetime asc
            """.format(id)

    with database.engine.connect() as con:
        rows = con.execute(sql)
        result = []
        for row in rows:
            result.append(row._asdict())
        return result


