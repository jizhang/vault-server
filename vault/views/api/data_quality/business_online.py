from flask import Response
from flask_login import login_required

from vault import db
from vault.models.business_online import BusinessOnline
from vault.services import user as user_svc
from vault.services.data_quality import business_online as biz_service
from vault.services.meta import meta_db
from vault.utils import get_arg, get_form, row_to_dict, rows_to_list
from vault.views.api import RequestError, exports, make_api_response


@exports('/data-quality/business-online/list', methods=['GET'])
@login_required
def business_online_list() -> Response:
    rows = biz_service.get_list()
    data = rows_to_list(rows)

    user_ids = set(row.user_id for row in rows)
    usernames = user_svc.get_usernames(user_ids)
    for item in data:
        if item['user_id'] in usernames:
            item['username'] = usernames[item['user_id']]
        else:
            item['username'] = '-'

    return make_api_response({'data': data})


@exports('/data-quality/business-online/save', methods=['POST'])
@login_required
def business_online_save() -> Response:
    row_id = get_form('id', type=int, default=0)
    title = get_form('title')
    user_id = get_form('user_id', type=int)
    status = get_form('status', type=int,
                      choices=[BusinessOnline.STATUS_OK, BusinessOnline.STATUS_PAUSED])
    db_id = get_form('db_id', type=int)
    query = get_form('query')

    if row_id and not biz_service.exists(row_id):
        raise RequestError('记录不存在')

    if user_svc.get_user(user_id) is None:
        raise RequestError('用户不存在')

    if not meta_db.db_exists(db_id):
        raise RequestError('数据库不存在')

    row = BusinessOnline()
    row.id = row_id
    row.title = title
    row.user_id = user_id
    row.status = status
    row.db_id = db_id
    row.query = query

    biz_service.save(row)
    db.session.commit()

    return make_api_response({
        'id': row.id,
    })


@exports('/data-quality/business-online/delete', methods=['POST'])
@login_required
def business_online_delete() -> Response:
    row_id = get_form('id', type=int)

    if not biz_service.exists(row_id):
        raise RequestError('记录不存在')

    biz_service.delete(row_id)
    db.session.commit()

    return make_api_response('ok')


@exports('/data-quality/business-online/edit', methods=['GET'])
@login_required
def business_online_edit() -> Response:
    row_id = get_arg('id', type=int)

    row = biz_service.get(row_id)
    if row is None:
        raise RequestError('记录不存在')

    data = row_to_dict(row)
    return make_api_response({
        'data': data,
    })


@exports('/data-quality/business-online/check-query', methods=['POST'])
@login_required
def business_online_check_query() -> Response:
    db_id = get_form('db_id', type=int)
    query = get_form('query')

    try:
        output, _ = biz_service.check_business(db_id, query)
    except Exception as e:
        return make_api_response({
            'code': 400,
            'message': str(e),
        })
    else:
        return make_api_response({
            'code': 200,
            'message': output,
        })
