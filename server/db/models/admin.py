from db.models import db

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String)
    password = db.Column(db.String)