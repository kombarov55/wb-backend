from datetime import datetime

from smsactivate.api import SMSActivateAPI

from config import database, app_config
from model.phone_number import PhoneNumberVO, PhoneNumberStatus
from repository import phone_number_repository

sa = SMSActivateAPI(app_config.sms_activate_key)


def get_new_number():
    print("get new number")

    session = database.session_local()

    rs = sa.getNumber(service="uu", country=0, maxPrice=15, freePrice=True)
    # rs = json.loads('{"activation_id": 1178493145, "phone": 79862292048}')
    print(rs)
    vo = PhoneNumberVO(
        ext_id=rs["activation_id"],
        number=rs["phone"],
        status=PhoneNumberStatus.just_received,
        received_datetime=datetime.now(),
        status_change_datetime=datetime.now()
    )

    phone_number_repository.save(session, vo)

    print("received new number {}".format(vo.number))

    session.close()


def get_balance():
    rs = sa.getBalance()
    return rs["balance"]


def get_prices():
    rs = sa.getPrices(service="uu", country=0)
    return rs["0"]["uu"]["cost"]


