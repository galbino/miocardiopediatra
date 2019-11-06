import hashlib
import os
from app.models.User import User
from app.util.exceptions import *
from app.models.Especialidade import Especialidade
from app import db


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


def check_user_existance(user_id):
    return db.session.query(User.query.filter(User.id == user_id).exists()).scalar()


def get_especialidades():
    esp_list = Especialidade.query.all()
    return [esp.as_dict() for esp in esp_list]


def signup(json_file):
    user = User()
    user.cpf = json_file.get("cpf")
    user.name = json_file.get("nome")
    user.neighbourhood = json_file.get("bairro")
    user.city = json_file.get("cidade")
    user.gender = json_file.get("sexo")
    user.state = json_file.get("estado")
    user.phone = json_file.get("telefone")
    try:
        user.password = encrypt_password(json_file.get("senha"))
    except Exception:
        raise WeakPassword
    user.is_doctor = json_file.get("isDoctor")
    user.date_of_birth = json_file.get("dataNascimento")
    user.email = json_file.get("email")
    if user.is_doctor == 1:
        user.crm = json_file.get("crm")
        user.esp_id = json_file.get("especialidade")
    elif user.is_doctor == 0:
        user.height = json_file.get("altura")
        user.weight = json_file.get("peso")
        user.phone_resp = json_file.get("telefoneResponsavel")
        user.email_resp = json_file.get("emailResponsavel")
        user.obs = json_file.get("observacoes")
    else:
        raise BadRequest
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        print(err)
        raise BadRequest
    return "Sucesso"
