from db.models import db

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer(), primary_key=True)
    