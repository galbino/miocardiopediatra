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
    phone = db.Column(db.String(30))
    state = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    city = db.Column(db.String(30))
    neighbourhood = db.Column(db.String(30))
    is_doctor = db.Column(TINYINT)
    date_of_birth = db.Column(db.DATETIME)

    # Colunas de pacientes
    phone_resp = db.Column(db.String(30))
    cpf_resp = db.Column(db.String(15))
    height = db.Column(db.String(5))
    weight = db.Column(db.String(10))
    email_resp = db.Column(db.String(200), unique=True)
    obs = db.Column(db.String(500))

    # Colunas do médico
    crm = db.Column(db.String(15), unique=True)
    esp_id = db.Column(BIGINT(unsigned=True), db.ForeignKey("Especialidade.id"))

    last_update = db.Column(db.DATETIME, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DATETIME, default=datetime.utcnow)

    especialidade = db.relationship("Especialidade", lazy='select', cascade='delete, save-update')

    def __init__(self):
        self.id = uuid1().int >> 64

    @property
    def id_(self):
        return str(self.id)

    def as_dict(self):
        resp = {"id": self.id_, "name": self.name, "cpf": self.cpf, "email": self.email,
                "last_update": self.last_update, "telefone": self.phone, "estado": self.state,
                "bairro": self.neighbourhood, "is_doctor": self.is_doctor}
        if self.is_doctor:
            resp = {**resp, "crm": self.crm, "especialidade": {"id": self.especialidade.id,
                                                               "name": self.especialidade.name} if self.especialidade else None}
        else:
            resp = {**resp, "cpf_resp": self.cpf_resp, "tel_resp": self.phone_resp, "altura": self.height, "peso": self.weight, "obs": self.obs}
            pass
        return resp

