from flask import Flask
from flask_cors import CORS
from environment.config import *
from flask_sqlalchemy import SQLAlchemy

config = Config()
app = Flask(__name__)
CORS(app)
csp = {
}

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app=app)

from app import models
from app.controllers import default
