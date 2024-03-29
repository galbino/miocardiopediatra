from app import app
import json
import os
from flask import jsonify, request
from app.services import user_services, auth_service, faq_services, exame_services
from app.util.decorator import requires_authn, requires_authz
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
@requires_authz
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
@requires_authz
def get_patient(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        resp["data"] = user_services.get_user_as_dict(_id, 0)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/anamnese/<_id>', methods=['DELETE'])
@requires_authn
@requires_authz
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
@requires_authz
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
@requires_authz
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
@requires_authz
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
@requires_authz
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
@requires_authz
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
        resp["data"] = user_services.get_user_as_dict(own_id)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/profile', methods=['PATCH'])
@requires_authn
def update_profile(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    own_id = kwargs.get("user_id")
    try:
        resp["data"] = user_services.patch_user(own_id, request.json)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/faq', methods=['GET'])
@requires_authn
def list_questions(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    answered = request.args.get("answered")
    try:
        resp["data"] = faq_services.list_faq(answered)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/faq', methods=['POST'])
@requires_authn
def ask_question(**kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    question = request.json.get("question")
    uid = kwargs.get("user_id")
    try:
        resp["data"] = faq_services.create_question(uid, question)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/faq/<_id>', methods=['PATCH'])
@requires_authn
@requires_authz
def answer_question(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    answer = request.json.get("answer")
    uid = kwargs.get("user_id")
    try:
        resp["data"] = faq_services.answer_question(_id, answer, uid)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/faq/<_id>', methods=['DELETE'])
@requires_authn
@requires_authz
def delete_question(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    try:
        resp["data"] = faq_services.delete_faq(_id)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)


@app.route('/user/<_id>/exam', methods=['POST'])
@requires_authn
@requires_authz
def add_exam_to_user(_id, **kwargs):
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    uid = kwargs.get("user_id")
    exams = request.json.get("exam_list")
    try:
        resp["data"] = exame_services.create_user_exame(_id, exams, uid)
    except AbroadException as err:
        resp["errors"] = [erro for erro in err.args]
    return jsonify(resp)