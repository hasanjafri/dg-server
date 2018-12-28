from db.models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String)
    password = db.Column(db.String)
    project_id = db.Column(None, db.ForeignKey('projects.id'))