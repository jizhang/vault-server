from vault import db


class BusinessOnline(db.Model):
    __tablename__ = 't_business_online'

    STATUS_OK = 1
    STATUS_PAUSED = 2
    STATUS_DELETED = 99

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    db_id = db.Column(db.Integer)
    query = db.Column(db.String)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
