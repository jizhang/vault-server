from flask import Response
from flask_login import login_required

from vault import db, utils
from vault.models.meta_db import MetaDb
from vault.views.api import exports, make_api_response


@exports('/meta/db/list', methods=['GET'])
@login_required
def meta_db_list() -> Response:
    rows = db.session.query(MetaDb).\
        filter_by(status=MetaDb.STATUS_ONLINE).\
        order_by(MetaDb.create_time.desc()).\
        all()

    dbs = []
    for row in rows:
        dbs.append({
            'id': row.id,
            'db_alias': row.db_alias,
            'db_type': row.db_type,
            'db_url': row.db_url,
            'create_time': utils.format_datetime(row.create_time),
            'update_time': utils.format_datetime(row.update_time),
        })

    return make_api_response(dbs)
