import json

from flask import Flask, request
from flask_cors import CORS

import task_request_service
from config import database
from config.alchemy_encoder import AlchemyEncoder
from repository import phone_number_repository, task_request_repository, proxy_repository, task_repository
from service import sms_activate

app = Flask(__name__)
cors = CORS(app, send_wildcard=True)

database.base.metadata.create_all(bind=database.engine)

@app.route('/')
def hello_world():
    return 'Hello Worldente!'


@app.route("/task_request", methods=["GET", "POST"])
def post_task_request():
    if request.method == "POST":
        body = request.get_json()
        task_request_service.process(body)
        return "OK"
    if request.method == "GET":
        return task_request_repository.get_all()


@app.route("/task_request/tasks")
def tasks():
    id = int(request.args.get("id"))
    return task_repository.find_by_task_request_id(id)


@app.route("/phones")
def get_phones():
    with database.session_local() as session:
        return json.dumps(phone_number_repository.get_all(session), cls=AlchemyEncoder)


@app.route("/phones_data")
def get_phones_data():
    balance = sms_activate.get_balance()
    return {
        "balance": balance
    }


@app.route("/request_phone", methods=["POST"])
def post_request_phone():
    body = request.get_json()
    amount = int(body["amount"])
    for i in range(0, amount):
        sms_activate.get_new_number()
    return {
        "status": "OK"
    }


@app.route("/available_numbers", methods=["GET"])
def available_numbers():
    amount = phone_number_repository.count_activated()
    return {
        "amount": amount
    }


@app.route("/proxy", methods=["GET", "POST", "DELETE"])
def proxy():
    with database.session_local() as session:
        if request.method == "GET":
            offset = int(request.args.get("offset"))
            limit = int(request.args.get("limit"))
            return json.dumps(proxy_repository.get_all(session, offset, limit), cls=AlchemyEncoder)
        if request.method == "POST":
            body = request.get_json()
            proxy_repository.save(session, body)
            return {
                "status": "OK"
            }
        if request.method == "DELETE":
            id = int(request.args.get("id"))
            proxy_repository.delete(id)
            return {
                "status": "OK"
            }


if __name__ == '__main__':
    app.run()

