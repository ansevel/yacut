from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .constants import MAX_SHORT_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import check_custom_id, get_unique_short_id


@app.route('/api/id/<string:short_id>/')
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original})


@app.route('/api/id/', methods=['POST'])
def add_urlmap():
    data = request.get_json()
    if not request.data:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    if data.get('custom_id'):
        custom_id = data['custom_id']
        if len(custom_id) > MAX_SHORT_LENGTH or not check_custom_id(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки',
                HTTPStatus.BAD_REQUEST
            )
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.',
                HTTPStatus.BAD_REQUEST
            )
    else:
        data['custom_id'] = get_unique_short_id()
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    short_link = url_for('index_view', _external=True) + urlmap.short
    return (
        jsonify({'url': urlmap.original, 'short_link': short_link}),
        HTTPStatus.CREATED
    )
