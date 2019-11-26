from app.models.FAQ import *
from app import db
from app.util.exceptions import *


def list_faq(answered):
    resp = FAQ.query.filter(FAQ.answered == answered).all()
    faq_list = [faq.as_dict() for faq in resp]
    return faq_list


def get_faq(faq_id):
    faq = FAQ.query.filter(FAQ.id == faq_id).first()
    if faq:
        return faq
    else:
        raise NotFound


def create_question(user_id, question):
    faq = FAQ()
    faq.question = question
    faq.asked_by = user_id
    faq.answered = 0
    try:
        db.session.add(faq)
        db.session.commit()
        return faq.as_dict_new()
    except Exception as err:
        print(err)
        db.session.rollback()
        raise BadRequest


def answer_question(faq_id, answer, doctor_id):
    faq = get_faq(faq_id)
    faq.answer = answer
    faq.answered_by = doctor_id
    faq.answered = 1
    try:
        db.session.commit()
        return faq.as_dict()
    except Exception as err:
        print(err)
        db.session.rollback()
        raise BadRequest


def delete_faq(faq_id):
    faq = get_faq(faq_id)
    try:
        db.session.delete(faq)
        db.session.commit()
        return faq.as_dict()
    except Exception as err:
        print(err)
        db.session.rollback()
        raise BadRequest
