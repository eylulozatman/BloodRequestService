from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(10), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    num_of_units = db.Column(db.Integer, nullable=False)
    duration_of_search = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(100), nullable=False)