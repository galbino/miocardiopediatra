import hashlib
import os
from app.models.Anamnese import *
from app.models.User import User
from app.util.exceptions import *
from app.services import exame_services
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


def list_users(is_doctor, query):
    resp = User.query.filter(User.is_doctor == is_doctor)
    if query:
        resp = resp.filter(User.name.like("%" + query + "%"))
    resp = resp.all()
    patient_list = [patient.as_dict_short() for patient in resp]
    return patient_list


def get_user_as_dict(_id, is_doctor=None):
    resp = User.query.filter(User.id == _id)
    if is_doctor:
        resp = resp.filter(User.is_doctor == is_doctor)
    resp = resp.first()
    if resp:
        return resp.as_dict()
    else:
        raise NotFound


def get_user(_id, is_doctor=None):
    resp = User.query.filter(User.id == _id)
    if is_doctor:
        resp = resp.filter(User.is_doctor == is_doctor)
    resp = resp.first()
    if resp:
        return resp
    else:
        raise NotFound


def check_user_existance(user_id):
    return db.session.query(User.query.filter(User.id == user_id).exists()).scalar()


def list_especialidades():
    esp_list = Especialidade.query.all()
    return [esp.as_dict() for esp in esp_list]


def signup(json_file):
    user = User()
    try:
        user.name = json_file["nome"]
        user.cpf = json_file["cpf"]
        user.email = json_file["email"]
    except Exception:
        raise LackOfParameters
    user.neighbourhood = json_file.get("bairro")
    user.city = json_file.get("cidade")
    user.gender = json_file.get("sexo")
    user.state = json_file.get("estado")
    user.phone = json_file.get("telefone")
    try:
        user.password = encrypt_password(json_file["senha"])
    except Exception:
        raise WeakPassword
    user.is_doctor = json_file.get("isDoctor")
    user.date_of_birth = json_file.get("dataNascimento")
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
        db.session.rollback()
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
        taxa_it, taxa_ia = calc_taxa_from_questions(anamnese.as_dict_calc())
        exames = []
        if taxa_it:
            exames.extend(exame_services.list_exames(for_it=1))
        if taxa_ia:
            exames.extend(exame_services.list_exames(for_ia=1))
        return {**anamnese.as_dict(lang), "miocardite_rate": taxa_it, "miocardiopatia_rate": taxa_ia, "exams": exames}
    except Exception as err:
        print(err)
        db.session.rollback()
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


def get_anamnese_as_text(anamnese_id, doctor_id, lang="pt-BR"):
    anamnese = UserAnamnese.query.filter(UserAnamnese.id == anamnese_id).filter(UserAnamnese.doctor_id == doctor_id).first()
    if anamnese:
        return anamnese.as_dict(lang)
    else:
        raise NotFound


def get_anamnese(anamnese_id, doctor_id):
    anamnese = UserAnamnese.query.filter(UserAnamnese.id == anamnese_id).filter(UserAnamnese.doctor_id == doctor_id).first()
    if anamnese:
        return anamnese
    else:
        raise NotFound


def delete_anamnese(anamnese_id, doctor_id):
    resp = UserAnamnese.query.filter(UserAnamnese.id == anamnese_id).filter(UserAnamnese.doctor_id == doctor_id).delete()
    if resp == 0:
        raise NotFound
    db.session.commit()
    return True


def patch_anamnese(anamnese_id, doctor_id, entries, lang="pt-BR"):
    try:
        resp = get_anamnese(anamnese_id, doctor_id)
        UserAnamneseAnswers.query.filter(UserAnamneseAnswers.user_anamnese_id == anamnese_id).delete()
        answers = fill_questions(entries)
        resp.answers.extend(answers)
        db.session.commit()
        taxa_it, taxa_ia = calc_taxa_from_questions(resp.as_dict_calc())
        exames = []
        if taxa_it:
            exames.extend(exame_services.list_exames(0))
        if taxa_ia:
            exames.extend(exame_services.list_exames(1))
        return {**resp.as_dict(lang), "miocardite_rate": taxa_it, "miocardiopatia_rate": taxa_ia, "exams": exames}
    except Exception as err:
        print(err)
        db.session.rollback()
        raise BadRequest


def calc_taxa_from_questions(questions):
    taxa_miocardite = 0
    taxa_miocardiopatia = 0
    overall_weight_it = 0
    overall_weight_ia = 0
    for question in questions:
        weight_ia = question.get("weight_miocardiopatia")
        value_ia = question.get("value_weight_miocardiopatia")
        weight_it = question.get("weight_miocardite")
        value_it = question.get("value_weight_miocardite")
        answer = question.get("answer")
        if answer == value_ia:
            taxa_miocardiopatia += 1 * weight_ia
        if answer == value_it:
            taxa_miocardite += 1 * weight_it
        overall_weight_it += weight_it
        overall_weight_ia += weight_ia
    resp_it = taxa_miocardite / overall_weight_it
    resp_ia = taxa_miocardiopatia / overall_weight_ia
    return resp_it, resp_ia


def patch_user(user_id, req):
    user = get_user(user_id)
    user.name = req.get("name")
    user.phone = req.get("phone")
    user.state = req.get("state")
    user.gender = req.get("gender")
    user.city = req.get("city")
    user.neighbourhood = req.get("neighbourhood")
    if user.is_doctor:
        user.esp_id = req.get("specialty_id")
        user.crm = req.get("crm")
    else:
        user.phone_resp = req.get("phone_resp")
        user.height = req.get("height")
        user.weight = req.get("weight")
        user.obs = req.get("obs")
    db.session.commit()
    return user.as_dict()
