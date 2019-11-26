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
    resp['data'] = user_services.list_especialidades()
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
    query = request.args.get("q")
    try:
        resp["data"] = user_services.list_users(0, query)
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


@app.route('/anamnese/<_id>', methods=['DELETE'])
@requires_authn
def delete_anamnese(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    uid = kwargs.get("user_id")
    try:
        resp["data"] = user_services.delete_anamnese(_id, uid)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/anamnese/<_id>', methods=['PATCH'])
@requires_authn
def patch_anamnese(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    entries = request.json.get("questions")
    doctor_id = kwargs.get("user_id")
    try:
        resp["data"] = user_services.patch_anamnese(_id, doctor_id, entries)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/anamnese', methods=['POST'])
@requires_authn
def create_anamnese(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    user_id = request.json.get("patient_id")
    doctor_id = kwargs.get("user_id")
    template_id = request.json.get("template_id")
    entries = request.json.get("questions")
    try:
        resp["data"] = user_services.create_anamnese(user_id, doctor_id, template_id, entries)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/anamnese/<_id>', methods=['GET'])
@requires_authn
def get_anamnese(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    doctor_id = kwargs.get("user_id")
    try:
        resp["data"] = user_services.get_anamnese_as_text(_id, doctor_id)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/anamnese', methods=['GET'])
@requires_authn
def list_anamnese(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    doctor_id = kwargs.get("user_id")
    try:
        resp["data"] = user_services.list_all_anamneses(doctor_id)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/user/<_id>/anamnese', methods=['GET'])
@requires_authn
def list_anamnese_from_patient(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    doctor_id = kwargs.get("user_id")
    try:
        resp["data"] = user_services.list_all_anamneses_from_patient(_id, doctor_id)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/anamnese/template', methods=['GET'])
@requires_authn
def list_anamnese_template(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        resp["data"] = user_services.list_anamnese_template()
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/anamnese/template/<_id>', methods=['GET'])
@requires_authn
def get_anamnese_template(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        resp["data"] = user_services.get_anamnese_template(_id)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/profile', methods=['GET'])
@requires_authn
def get_profile(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    own_id = kwargs.get("user_id")
    try:
        resp["data"] = user_services.get_user(own_id)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)
