from vault import db


class MetaDb(db.Model):
    __tablename__ = 't_meta_db'

    STATUS_ONLINE = 1
    STATUS_DELETED = 99

    TYPE_MYSQL = 1

    id = db.Column(db.Integer, primary_key=True)
    db_alias = db.Column(db.String)
    db_type = db.Column(db.Integer)
    db_url = db.Column(db.String)
    status = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
