from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Personne(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    addresse = db.Column(db.String(100))
    telephone = db.Column(db.String(10), unique=True)
    img_path = db.Column(db.String(150))
    signings =db.relationship('Signing', backref='personne', lazy=True)

class Signing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personne_id = db.Column(db.Integer, db.ForeignKey("personne.id"), nullable=False)
    signer_host = db.Column(db.String(100))
    signer_ip = db.Column(db.String(100))
    signing_date = db.Column(db.Date)
    signing_updated = db.Column(db.Date)