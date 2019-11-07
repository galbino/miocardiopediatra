from app.util.exceptions import *
from app.services.user_services import encrypt_password, get_user_by_email_pw
from app import app
import itsdangerous


def login(email, password):
    try:
        user = get_user_by_email_pw(email, encrypt_password(password))
        token = generate_auth_token(user.id, user.is_doctor)
    except NotFound:
        raise LoginIncorrect
    return user.as_dict_short(), token


def generate_auth_token(user_id, is_doctor):
    serial = itsdangerous.TimedJSONWebSignatureSerializer(app.secret_key, expires_in=3600)
    return serial.dumps({'user_id': user_id, 'is_doctor': is_doctor}).decode("ascii")


def retrieve_auth_token_info(token):
    try:
        serial = itsdangerous.TimedJSONWebSignatureSerializer(app.secret_key)
        data = serial.loads(token)
        return data
    except (itsdangerous.BadSignature, itsdangerous.exc.SignatureExpired):
        raise InvalidToken
