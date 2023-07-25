from functools import wraps
from typing import Tuple

from flask import Response, jsonify

from vault import app


def exports(rule, **options):
    """
    所有 API 都使用这个 decorator
    """
    def decorator(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            app.logger.debug('API: %s.%s' % (fn.__module__, fn.__name__))
            return fn(*args, **kwargs)

        api_rule = '{}/api{}'.format(app.config['APPLICATION_ROOT'], rule)
        endpoint = options.pop('endpoint', api_rule)
        app.add_url_rule(api_rule, endpoint, view_func=decorated_view, **options)
        return decorated_view
    return decorator


def make_api_response(payload: dict) -> Response:
    data = {
        'status': 'ok',
        'payload': payload,
    }
    return jsonify(data)


class RequestError(Exception):
    def __init__(self, message: str, code=400):
        super().__init__(message)
        self.message = message
        self.code = code


@app.errorhandler(RequestError)
def handle_request_error(error: RequestError) -> Tuple[Response, int]:
    data = {
        'code': error.code,
        'message': error.message,
    }
    return jsonify(data), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'status': 'fail',
        'err_code': 401,
        'err_msg': '未登陆',
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'status': 'fail',
        'err_code': 403,
        'err_msg': '没有权限',
    }), 403


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        'status': 'fail',
        'err_code': 404,
        'err_msg': '服务不存在',
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'status': 'fail',
        'err_code': 500,
        'err_msg': '出错了',
    }), 500


@app.route('/api/ping')
def ping():
    return 'pong'
