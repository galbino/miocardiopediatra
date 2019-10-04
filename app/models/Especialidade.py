from app import db
from uuid import uuid1
from sqlalchemy.dialects.mysql import BIGINT


class Especialidade(db.Model):
    __tablename__ = "Especialidade"
    id = db.Column("id", BIGINT(unsigned=True), primary_key=True)
    name = db.Column(db.String(60))

    def __init__(self):
        self.id = uuid1().int >> 64

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self):
        return {"id": self.id_, "name": self.name}