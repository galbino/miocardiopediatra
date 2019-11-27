from app import db
from uuid import uuid1
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from datetime import datetime
from enum import Enum


class Exame(db.Model):
    __tablename__ = "Exame"
    id = db.Column("id", BIGINT(unsigned=True), primary_key=True)
    name = db.Column(db.String(50))
    cardiomiopatia = db.Column(TINYINT)
    miocardite = db.Column(TINYINT)

    def __init__(self):
        self.id = uuid1().int >> 64

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self):
        return {"id": self.id_, "name": self.name}


class UserExame(db.Model):
    __tablename__ = "UserExame"
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("User.id"))
    exame_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("Exame.id"))
    requested_by = db.Column(BIGINT(unsigned=True), db.ForeignKey("User.id"))
    status = db.Column(TINYINT)
    exame = db.relationship("Exame", lazy='select')
    doctor = db.relationship("User", lazy='select', primaryjoin="User.id == UserExame.requested_by")

    def __init__(self):
        self.id = uuid1().int >> 64
        self.status = -1

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self):
        return {**self.exame.as_dict(), "status": ExameStatus(self.status).name}


class ExameStatus(Enum):
    PENDING = -1
    DONE = 1
    REJECTED = 0
