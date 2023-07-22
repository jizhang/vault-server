import hashlib
from typing import Dict, Iterable, Optional, Union

from vault import db
from vault.models.user import User


def get_user(user_id: Union[int, str]) -> Optional[User]:
    """Get user by ID."""
    return db.session.query(User).get(user_id)


def get_usernames(user_ids: Iterable[int]) -> Dict[int, str]:
    """Get usernames by ID list."""
    rows = db.session.query(User).\
        filter(User.id.in_(list(user_ids))).\
        all()
    return {row.id: row.username for row in rows}


def login_user(username: str, password: str) -> Optional[User]:
    """Verify username and password."""
    return db.session.query(User).\
        filter_by(username=username).\
        filter_by(password=get_password_digest(password)).\
        filter_by(status=1).\
        first()


def get_password_digest(password: str) -> str:
    """Get salted password digest."""
    m = hashlib.md5()
    m.update(f'PJNWkH0g4S{password}'.encode())
    return m.hexdigest()
