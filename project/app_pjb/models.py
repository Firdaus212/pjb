from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Pltainfo(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    elevasi_akhir = db.Column(db.Float)
    elevasi_awal = db.Column(db.Float)
    elevasi_target = db.Column(db.Float)
    inflow_outflow_mendalan = db.Column(db.Float)
    inflow_selorejo = db.Column(db.Float)
    inflow_siman = db.Column(db.Float)
    limpas = db.Column(db.Float)
    mw_mendalan = db.Column(db.Float)
    mw_mendalan_1 = db.Column(db.Float)
    mw_mendalan_2 = db.Column(db.Float)
    mw_mendalan_3 = db.Column(db.Float)
    mw_mendalan_4 = db.Column(db.Float)
    mw_selorejo = db.Column(db.Float)
    mw_siman = db.Column(db.Float)
    mw_siman_1 = db.Column(db.Float)
    mw_siman_2 = db.Column(db.Float)
    mw_siman_3 = db.Column(db.Float)
    mwh_mendalan = db.Column(db.Float)
    mwh_selorejo = db.Column(db.Float)
    mwh_siman = db.Column(db.Float)
    outflow_selorejo = db.Column(db.Float)
    suplesi_siman = db.Column(db.Float)