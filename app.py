from flask import Flask, request
from flask_cors import CORS, cross_origin

import task_request_service
from config import database

app = Flask(__name__)
cors = CORS(app, send_wildcard=True)

database.base.metadata.create_all(bind=database.engine)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/task_request", methods=["GET", "POST"])
def post_task_request():
    if request.method == "POST":
        body = request.get_json()
        task_request_service.process(body)
        return "ХОрошо"
    if request.method == "GET":
        print("GET")
        return "OK"


if __name__ == '__main__':
    app.run()
