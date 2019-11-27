from flask import request, jsonify
from functools import wraps
from app.util.exceptions import *
from app.services import auth_service, user_services
import os
import json


def requires_authn(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        resp = json.loads(os.environ.get("RESPONSE_STRUCT"))
        access_token = request.headers.get('Authorization')
        try:
            if not access_token:
                raise AccessTokenMissing
            info = auth_service.retrieve_auth_token_info(access_token)
            if not info:
                raise InvalidToken
            user_id = info.get("user_id")
            if not user_services.check_user_existance(user_id):
                raise InvalidToken
            kwargs["user_id"] = user_id
            kwargs["is_doctor"] = info.get("is_doctor")
        except AbroadException as err:
            resp['errors'] = [errors for errors in err.args]
            return jsonify(resp)
        kwargs['Authorization'] = access_token
        return f(*args, **kwargs)
    return decorated


def requires_authz(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        is_doctor = kwargs.get("is_doctor")
        if not is_doctor:
            raise Forbidden
        return f(*args, **kwargs)
    return decorated
