from flask_login import login_required, current_user

from vault import db
from vault.models.user import User
from vault.views.api import make_api_response, exports


@exports('/user/list', methods=['GET'])
@login_required
def user_list() -> tuple:
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
