from flask import Response
from flask_login import current_user, login_required

from vault import db
from vault.models.user import User
from vault.views.api import exports, make_api_response


@exports('/user/list', methods=['GET'])
@login_required
def user_list() -> Response:
    rows = db.session.query(User).\
        filter_by(status=1).\
        order_by(User.username.asc()).\
        all()

    users = []
    for row in rows:
        users.append({
            'id': row.id,
            'username': row.username,
            'is_current': 1 if str(row.id) == current_user.get_id() else 0,
        })

    return make_api_response(payload=users)
