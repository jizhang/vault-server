from typing import List, Optional, Tuple
from datetime import datetime, timedelta

from vault import db
from vault.models.meta_db import MetaDb
from vault.models.business_online import BusinessOnline
from vault.services.meta import meta_db


def exists(row_id: int) -> bool:
    row = db.session.query(BusinessOnline).get(row_id)
    return row is not None


def get_list() -> List[BusinessOnline]:
    return db.session.query(BusinessOnline).\
        filter(BusinessOnline.status != BusinessOnline.STATUS_DELETED).\
        order_by(BusinessOnline.created_at.desc()).\
        all()


def save(row: BusinessOnline):
    if row.id:
        db.session.merge(row)
    else:
        row.id = None
        row.created_at = datetime.now()
        db.session.add(row)


def delete(row_id: int):
    row = db.session.query(BusinessOnline).get(row_id)
    row.status = BusinessOnline.STATUS_DELETED


def get(row_id: int) -> Optional[BusinessOnline]:
    return db.session.query(BusinessOnline).get(row_id)


def check_business(db_id: int, query: str) -> Tuple[str, bool]:
    mdb = db.session.query(MetaDb).get(db_id)
    if mdb is None:
        raise ValueError('Meta DB not found.')

    sqls = [sql.strip() for sql in query.split(';') if sql.strip()]
    if not sqls:
        raise ValueError('Query cannot be empty.')

    date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    output = []
    has_data = False
    with meta_db.connect(mdb) as engine:
        for index, sql in enumerate(sqls):
            output.append(f'Query {index + 1}:')
            sql = sql.replace('{date}', date)
            sql = sql.replace('%', '%%')
            rows = engine.execute(sql).fetchall()
            if rows:
                for row in rows:
                    output.append(', '.join(str(col) for col in row))
                    if any(row):
                        has_data = True
            else:
                output.append('No result.')

            output.append('')

    return '\n'.join(output), has_data
