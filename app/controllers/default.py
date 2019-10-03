from app import app
import json
import os
from flask import jsonify, request
from app.services import user_services


@app.route('/', methods=['GET'])
def home():
    return 'ok', 200


@app.route('/login', methods=['POST'])
def login():
    resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
    email = request.json.get("email")
    pw = request.json.get("password")
    resp['data'].append(user_services.login(email, pw))
    return jsonify(resp)
