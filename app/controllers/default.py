from app import app
import json
import os
from flask import jsonify, request
from app.services import user_services
from app.util.exceptions import AbroadException


@app.route('/', methods=['GET'])
def home():
    return 'ok', 200


@app.route('/login', methods=['POST'])
def login():
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    email = request.json.get("email")
    pw = request.json.get("password")
    resp['data'] = user_services.login(email, pw)
    return jsonify(resp)


@app.route('/especialidade', methods=['GET'])
def get_especialidades():
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    resp['data'] = user_services.get_especialidades()
    return jsonify(resp)


@app.route('/signup', methods=['POST'])
def signup():
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        req_json = request.get_json()
        resp['data'] = user_services.signup(req_json)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)
