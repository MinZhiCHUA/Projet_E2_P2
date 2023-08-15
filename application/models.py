
from flask_sqlalchemy import SQLAlchemy
#from . import db
# db = SQLAlchemy()
from .extension import db
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Predict(db.Model):

    # data={'Neighborhood':'GrnHill', 'TotRms_AbvGrd':7, 'Full_Bath':6, 'score_internal':1139, 'Year_Built':1988, 'Lot_Area':186812}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    id_user = db.Column(db.Integer)
    Neighborhood = db.Column(db.String(100))
    TotRms_AbvGrd = db.Column(db.Integer)
    Full_Bath = db.Column(db.Integer)
    score_internal = db.Column(db.Integer)
    Year_Built = db.Column(db.Integer)
    Lot_Area = db.Column(db.Integer)
    result = db.Column(db.Integer)

    # def __repr__(self):
    #     return f'{self.id} {self.id_user}'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


def init_db():
    print("Initialisation de la BDD")
    db.drop_all()
    db.create_all()
    User(email = "admin@gmail.com", name = "admin", password = generate_password_hash("1234", method="sha256")).save_to_db()
    # User(email = "admin@gmail.com", name = "admin", password = generate_password_hash("1234", method="sha256")).save_to_db()
    print("BDD initialisée")