from flask import abort, flash, redirect, render_template, jsonify

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if (custom_id and URLMap.query.filter_by(
                short=custom_id).first() is not None):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id or get_unique_short_id()
        )
        db.session.add(urlmap)
        db.session.commit()
        context = {
            'form': form,
            'urlmap': urlmap
        }
        return render_template('index.html', **context)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)


@app.route('/test/<string:id>')
def for_test(id):
    urlmap = URLMap.query.filter_by(short=id).first_or_404()
    return jsonify({'result': urlmap.original})
