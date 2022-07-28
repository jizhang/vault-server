import pkgutil
from typing import Iterable, List
from decimal import Decimal
from datetime import datetime

from flask import request
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.decl_api import DeclarativeMeta

from vault.views.api import APIException


def load_module_recursively(module) -> None:
    for _, name, ispkg in pkgutil.iter_modules(module.__path__):
        module_name = '%s.%s' % (module.__name__, name)
        print('loading view: %s' % module_name)
        _module = __import__(module_name, fromlist=[''])

        if ispkg:
            load_module_recursively(_module)


def get_param(data: dict, key: str, default=None, type=None, choices=None, help=None):
    """
    获取并检查参数

    :param data: 字典数据
    :param key: 键
    :param default: 默认值
    :param type: 参数类型
    :param choices: 可选值
    :param help: 错误信息
    """
    if help is None:
        help = 'invalid {}'.format(key)

    value = data.get(key)
    if not value:
        if default is None:
            raise APIException(help)
        return default

    if type is not None:
        try:
            value = type(value)
        except Exception:
            raise APIException(help)

    if choices is not None and value not in choices:
        raise APIException(help)

    return value


def get_arg(key: str, default=None, type=None, choices=None, help=None):
    return get_param(request.args, key, default, type, choices, help)


def get_form(key: str, default=None, type=None, choices=None, help=None):
    return get_param(request.form, key, default, type, choices, help)


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


def format_datetime(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')
