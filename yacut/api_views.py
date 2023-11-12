from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import check_custom_id, get_unique_short_id


@app.route('/api/id/<string:short_id>/')
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if not urlmap:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original})


@app.route('/api/id/', methods=['POST'])
def add_urlmap():
    data = request.get_json()
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    if data.get('custom_id'):
        custom_id = data['custom_id']
        if len(custom_id) > 16 or not check_custom_id(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки', 400)
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.', 400)
    else:
        data['custom_id'] = get_unique_short_id()
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    short_link = url_for('index_view', _external=True) + urlmap.short
    return jsonify({'url': urlmap.original, 'short_link': short_link}), 201
