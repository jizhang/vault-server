from vault import db


class DbInstance(db.Model):
    __tablename__ = 'db_instance'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    host = db.Column(db.String)
    port = db.Column(db.Integer)
    username = db.Column(db.String)
    password = db.Column(db.String)
    database = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
