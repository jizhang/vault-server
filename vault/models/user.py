from vault import db


class User(db.Model):
    __tablename__ = 't_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    nickname = db.Column(db.String)
    password = db.Column(db.String)
    is_active = db.Column('status', db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return "<User-{}: {}>".format(self.id, self.username)
