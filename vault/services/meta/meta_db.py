import contextlib
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from vault import db
from vault.models.meta_db import MetaDb


def db_exists(db_id: int) -> bool:
    row = db.session.query(MetaDb).get(db_id)
    return row is not None


@contextlib.contextmanager
def connect(mdb: MetaDb) -> Iterator[Engine]:
    engine = create_engine(mdb.db_url)
    try:
        yield engine
    finally:
        engine.dispose()
