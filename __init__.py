from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spectra.db"
db = SQLAlchemy()
db.init_app(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'riiijyvsh8aj6w7rnpxxoxatinn63tbamzdt6zb6ooyad3p5rwzmq2ykiq2hmduq'
admin = Admin(app, name='nRamanSpectra', template_mode='bootstrap4')

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'

import nRamanSpectra.views
