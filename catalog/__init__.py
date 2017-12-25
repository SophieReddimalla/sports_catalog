import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DQnp]}^$HSBnOfxwXaaXfr2V'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2:///catalog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

import models
import views