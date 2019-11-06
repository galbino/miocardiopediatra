from app import app
import json
import os
from flask import jsonify, request
from app.services import user_services, auth_service
from app.util.decorator import requires_authn
from app.util.exceptions import AbroadException


@app.route('/', methods=['GET'])
def home():
    return 'ok', 200


@app.route('/login', methods=['POST'])
def login():
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    email = request.json.get("email")
    pw = request.json.get("password")
    user, token = auth_service.login(email, pw)
    resp['data'] = {"token": {"access_token": token, "type": "bearer", "expires_in": 3600}, **user}
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


@app.route('/patient', methods=['GET'])
@requires_authn
def list_patients(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        resp["data"] = user_services.list_users(0)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/patient/<_id>', methods=['GET'])
@requires_authn
def get_patient(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        resp["data"] = user_services.get_user(_id, 0)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/patient/<_id>', methods=['PATCH'])
@requires_authn
def update_patient(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        pass
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/patient/<_id>', methods=['DELETE'])
@requires_authn
def delete_patient(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        pass
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)