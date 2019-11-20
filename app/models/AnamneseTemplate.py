from app import db
from uuid import uuid1
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from datetime import datetime


class AnamneseQuestion(db.Model):
    __tablename__ = "AnamneseQuestion"
    id = db.Column("id", BIGINT(unsigned=True), primary_key=True)
    label = db.Column(db.JSON)
    value_weight_miocardite = db.Column(TINYINT)
    value_weight_miocardiopatia = db.Column(TINYINT)
    weight_miocardite = db.Column(db.Integer)
    weight_miocardiopatia = db.Column(db.Integer)
    required = db.Column(TINYINT)
    template_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("AnamneseTemplate.id"))
    answers = db.relationship("UserAnamneseAnswers", lazy='select', cascade='delete, save-update')

    def __init__(self):
        self.id = uuid1().int >> 64

    @property
    def id_(self):
        return str(self.id)

    def get_label(self, lang):
        return self.label.get(lang)

    def as_dict(self, lang):
        return {"id": self.id_, "label": self.label.get(lang), "required": self.required}


class AnamneseTemplate(db.Model):
    __tablename__ = "AnamneseTemplate"
    id = db.Column("id", BIGINT(unsigned=True), primary_key=True)
    name = db.Column(db.String(500))
    questions = db.relationship("AnamneseQuestion", lazy='select', cascade='delete, save-update')

    def __init__(self):
        self.id = uuid1().int >> 64

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self):
        return {"id": self.id_, "name": self.name}

    def as_dict_template(self, lang):
        return {"id": self.id_, "name": self.name, "questions": [question.as_dict(lang) for question in self.questions]}


class UserAnamnese(db.Model):
    __tablename__ = "UserAnamnese"
    id = db.Column("id", BIGINT(unsigned=True), primary_key=True)
    template_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("AnamneseTemplate.id"), primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("User.id"), primary_key=True)
    doctor_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("User.id"), primary_key=True)
    last_update = db.Column(db.DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DATETIME, default=datetime.utcnow)
    answers = db.relationship("UserAnamneseAnswers", lazy='select', cascade="delete, delete-orphan, save-update")
    anamnese_template = db.relationship("AnamneseTemplate", lazy='select')
    user = db.relationship("User", lazy='select', primaryjoin="UserAnamnese.user_id == User.id")
    doctor = db.relationship("User", lazy='select', primaryjoin="UserAnamnese.doctor_id == User.id")

    @property
    def id_(self):
        return str(self.id)

    def __init__(self, template_id, user_id, doctor_id):
        self.id = uuid1().int >> 64
        self.template_id = template_id
        self.user_id = user_id
        self.doctor_id = doctor_id

    def as_dict_short(self):
        return {"template": self.anamnese_template.as_dict(), "user_id": self.user_id, "user_name": self.user.name, "creation_date": self.creation_date, "last_update": self.last_update, "anamnese_id": self.id_}

    def as_dict(self, lang):
        return {"template": self.anamnese_template.as_dict(), "user_id": self.user_id, "doctor_id": self.doctor_id, "questions": [answer.as_dict(lang) for answer in self.answers], "anamnese_id": self.id_}


class UserAnamneseAnswers(db.Model):
    __tablename__ = "UserAnamneseAnswers"
    user_anamnese_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("UserAnamnese.id", ondelete='CASCADE'), primary_key=True)
    question_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("AnamneseQuestion.id"), primary_key=True)
    answer = db.Column(TINYINT)
    question = db.relationship("AnamneseQuestion", lazy='select')
    user_anamnese = db.relationship("UserAnamnese", lazy='select')

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self, lang):
        return {"question": self.question.get_label(lang), "answer": self.answer}