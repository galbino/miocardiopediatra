import hashlib
import os
from app.models.AnamneseTemplate import *
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


def list_users(is_doctor):
    resp = User.query.filter(User.is_doctor == is_doctor).all()
    patient_list = [patient.as_dict_short() for patient in resp]
    return patient_list


def get_user(_id, is_doctor):
    resp = User.query.filter(User.is_doctor == is_doctor).filter(User.id == _id).first()
    if resp:
        return resp.as_dict()
    else:
        raise NotFound


def check_user_existance(user_id):
    return db.session.query(User.query.filter(User.id == user_id).exists()).scalar()


def list_especialidades():
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
    return user.as_dict_short()


def list_anamnese_template():
    templates = AnamneseTemplate.query.all()
    return [template.as_dict() for template in templates]


def get_anamnese_template(template_id, lang="pt-BR"):
    template = AnamneseTemplate.query.filter(AnamneseTemplate.id == template_id).first()
    if template:
        return template.as_dict_template(lang)
    else:
        raise NotFound


def create_anamnese(user_id, doctor_id, template_id, entries, lang="pt-BR"):
    try:
        anamnese = UserAnamnese(template_id, user_id, doctor_id)
        anamnese.user_id = user_id
        answers = fill_questions(entries)
        anamnese.answers.extend(answers)
        db.session.add(anamnese)
        db.session.commit()
        return anamnese.as_dict(lang)
    except Exception as err:
        print(err)
        raise BadRequest


def fill_questions(question_list):
    anamnese = []
    for question in question_list.keys():
        uaa = UserAnamneseAnswers()
        uaa.question_id = question
        uaa.answer = question_list.get(question)
        anamnese.append(uaa)
    return anamnese


def list_all_anamneses(doctor_id):
    resp = UserAnamnese.query.filter(UserAnamnese.doctor_id == doctor_id).all()
    return [an.as_dict_short() for an in resp]


def list_all_anamneses_from_patient(user_id, doctor_id):
    resp = UserAnamnese.query.filter(UserAnamnese.doctor_id == doctor_id).filter(UserAnamnese.user_id == user_id).all()
    return [an.as_dict_short() for an in resp]


def get_anamnese(anamnese_id, doctor_id, lang="pt-BR"):
    anamnese = UserAnamnese.query.filter(UserAnamnese.id == anamnese_id).filter(UserAnamnese.doctor_id == doctor_id).first()
    if anamnese:
        return anamnese.as_dict(lang)
    else:
        raise NotFound


def delete_anamnese(anamnese_id, doctor_id):
    resp = UserAnamnese.query.filter(UserAnamnese.id == anamnese_id).filter(UserAnamnese.doctor_id == doctor_id).delete()
    if resp == 0:
        raise NotFound
    db.session.commit()
    return True


def patch_anamnese(anamnese_id, entries, lang="pt-BR"):
    resp = UserAnamnese.query.filter(UserAnamnese.id == anamnese_id).filter(UserAnamnese.doctor_id == doctor_id).first()
    if resp is not None:
        resp.answers.clear()
        answers = fill_questions(entries)
        resp.answers.extend(answers)
    else:
        raise NotFound
    db.session.commit()
    return resp.as_dict(lang)
