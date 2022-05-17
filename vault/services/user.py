import hashlib
from typing import Any, Optional, Iterable, Dict
from collections import namedtuple

from vault import db
from vault.models.user import User


class SiteUser:
    User = namedtuple('User', ['id', 'username'])

    def __init__(self, user_obj: Dict[str, Any]):
        self.user = self.User(
            id=user_obj.get('id', 0),
            username=user_obj.get('nickname', 'hh')
        )

    @property
    def is_authenticated(self):
        return self.user is not None

    @property
    def is_active(self):
        return False if self.user is None else True

    @property
    def is_anonymous(self):
        return self.user is None

    def get_id(self):
        return 0 if self.user is None else self.user.id


class UserService:
    @staticmethod
    def get(user_id: int) -> Optional[SiteUser]:
        row = db.session.query(User).\
            filter_by(id=user_id).\
            filter_by(is_active=1).\
            first()

        if row is None:
            return None

        return SiteUser({
            'id': row.id,
            'username': row.username,
            'nickname': row.nickname,
        })

    @staticmethod
    def login(username: str, password: str) -> Optional[SiteUser]:
        row = db.session.query(User).\
            filter_by(username=username).\
            filter_by(password=UserService.get_password_digest(password)).\
            filter_by(is_active=1).\
            first()

        if row is None:
            return None

        return SiteUser({
            'id': row.id,
            'username': row.username,
            'nickname': row.nickname,
        })

    @staticmethod
    def get_usernames(user_ids: Iterable[int]) -> Dict[int, str]:
        rows = db.session.query(User).\
            filter(User.id.in_(list(user_ids))).\
            all()
        return {row.id: row.username for row in rows}

    @staticmethod
    def get_password_digest(password: str) -> str:
        m = hashlib.md5()
        m.update(f'PJNWkH0g4S{password}'.encode())
        return m.hexdigest()
