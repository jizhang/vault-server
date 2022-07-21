import pkgutil
from typing import Iterable, List
from decimal import Decimal
from datetime import datetime

from sqlalchemy.engine.row import Row
from sqlalchemy.orm.decl_api import DeclarativeMeta


def load_module_recursively(module) -> None:
    for _, name, ispkg in pkgutil.iter_modules(module.__path__):
        module_name = '%s.%s' % (module.__name__, name)
        print('loading view: %s' % module_name)
        _module = __import__(module_name, fromlist=[''])

        if ispkg:
            load_module_recursively(_module)


def row_to_dict(row) -> dict:
    if isinstance(row, Row):
        row_dict = dict(row)
    elif isinstance(row.__class__, DeclarativeMeta):
        row_dict = {c.name: getattr(row, c.name) for c in row.__table__.columns}
    else:
        raise ValueError('Unsupported row type.')

    for key, value in row_dict.items():
        if isinstance(value, Decimal):
            row_dict[key] = float(value)
        elif isinstance(value, datetime):
            row_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')

    return row_dict


def rows_to_list(rows: Iterable) -> List[dict]:
    return [row_to_dict(i) for i in rows]
