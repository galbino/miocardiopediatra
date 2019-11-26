from app import db
from uuid import uuid1
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from datetime import datetime


class FAQ(db.Model):
    __tablename__ = "FAQ"
    id = db.Column("id", BIGINT(unsigned=True), primary_key=True)
    question = db.Column(db.String(500))
    answer = db.Column(db.String(500))
    answered = db.Column(TINYINT)
    answered_by = db.Column(BIGINT(unsigned=True), db.ForeignKey("User.id"))
    asked_by = db.Column(BIGINT(unsigned=True), db.ForeignKey("User.id"))

    last_update = db.Column(db.DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DATETIME, default=datetime.utcnow)

    user = db.relationship("User", lazy='select', primaryjoin="FAQ.asked_by == User.id")
    doctor = db.relationship("User", lazy='select', primaryjoin="FAQ.answered_by == User.id")

    def __init__(self):
        self.id = uuid1().int >> 64

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self):
        return {"id": self.id_, "question": self.question, "answered": self.answered, "answer": self.answer, "last_update": self.last_update, "creation_date": self.creation_date, "asked_by": self.user.name, "answered_by": self.doctor.name if self.answered else None}

    def as_dict_new(self):
        return {"id": self.id_, "question": self.question, "asked_by": self.user.name}