from config import database
from service import sms_activate


if __name__ == "__main__":
    database.base.metadata.create_all(bind=database.engine)
    print(sms_activate.get_prices())
