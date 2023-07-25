from flask import Response, request
from flask_login import current_user, login_required, login_user, logout_user

from vault import app
from vault.services import user as user_svc
from vault.views.api import RequestError, exports, make_api_response


@exports('/login', methods=['POST'])
def login() -> Response:
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        raise RequestError('Username and password cannot be empty.')

    user = user_svc.login_user(username, password)
    if user is None:
        raise RequestError('Invalid username or password.')

    login_user(user)
    app.logger.info(f'{user.username} Login')

    return make_api_response({
        'id': user.id,
        'username': user.username,
    })


@exports('/logout', methods=['GET', 'POST'])
def logout() -> Response:
    logout_user()
    return make_api_response('ok')


@exports('/current-user')
@login_required
def get_current_user() -> Response:
    return make_api_response({
        'id': current_user.id,
        'username': current_user.username,
    })
