from sqlalchemy.orm import Session

from config import database
from model.phone_number import PhoneNumberVO


def save(session: Session, vo: PhoneNumberVO):
    session.add(vo)
    session.commit()
    session.refresh(vo)
    return vo


def get_all():
    with database.engine.connect() as con:
        rows = con.execute("""
        select id, ext_id, number, status,
        cast (extract(epoch from received_datetime) * 1000 as bigint),
        cast (extract(epoch from status_change_datetime) * 1000 as bigint)
        from phone_number
        order by status_change_datetime desc
        """)
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "ext_id": row[1],
                "number": row[2],
                "status": row[3],
                "received_datetime": row[4],
                "status_change_datetime": row[5]
            })
        return result


def count_info():
    with database.engine.connect() as con:
        rows = con.execute("""
        select 
        (select count(*) 
        from phone_number 
        where status = 'ACTIVATED') activated_count,
        (select count(*) 
        from phone_number 
        where status = 'JUST_RECEIVED') just_received_count,
        (select count(*) 
        from phone_number 
        where status = 'ACTIVATING') activating_count
        """)
        result = []
        for row in rows:
            result.append({
                "activated": row[0],
                "just_received": row[1],
                "activating": row[2]
            })
        if len(result) == 0:
            return None
        else:
            return result[0]


def count_activated():
    with database.engine.connect() as con:
        rows = con.execute("select count(*) from phone_number where status = 'ACTIVATED'")
        result = []
        for row in rows:
            result.append(row[0])
        if len(result) == 0:
            return None
        else:
            return result[0]

