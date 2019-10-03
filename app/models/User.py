from app import db
from uuid import uuid1
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from datetime import datetime


class User(db.Model):
    __tablename__ = "User"
    id = db.Column("id", BIGINT(unsigned=True), primary_key=True)
    name = db.Column(db.String(60))
    cpf = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    telefone = db.Column(db.String(30))
    estado = db.Column(db.String(30))
    cidade = db.Column(db.String(30))
    bairro = db.Column(db.String(30))
    is_doctor = db.Column(TINYINT)

    last_update = db.Column(db.DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DATETIME, default=datetime.utcnow)

    def __init__(self):
        self.id = uuid1().int >> 64

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self):
        return {"id": self.id_, "name": self.name, "cpf": self.cpf, "email": self.email, "last_update": self.last_update,
                "telefone": self.telefone, "estado": self.estado, "bairro": self.bairro, "is_doctor": self.is_doctor}
