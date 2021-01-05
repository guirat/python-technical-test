import connexion
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Session = sessionmaker()

basedir = os.path.abspath(os.path.dirname(__file__))
connexion_app = connexion.App(__name__, specification_dir='specification')

app = connexion_app.app

db_url = "sqlite:////" + os.path.join(basedir, 'vms.db')

engine = create_engine(db_url)
Session.configure(bind=engine)
session = Session()

# Configure the SQLAlchemy
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

