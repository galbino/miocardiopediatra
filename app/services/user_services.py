import hashlib
import os
from app.models.User import User
from app.util.exceptions import *


def encrypt_password(password):
    hash_ = hashlib.sha256(os.environ.get('SALT').encode('utf-8'))
    hash_.update(password.encode('utf-8'))
    new_password = hash_.hexdigest()
    return new_password


def get_user_by_email_pw(email, password):
    user = User.query.filter(User.email == email).filter(User.password == password).first()
    if user:
        return user
    raise NotFound


def login(email, password):
    try:
        user = get_user_by_email_pw(email, encrypt_password(password))
    except NotFound:
        raise LoginIncorrect
    return user.as_dict()
