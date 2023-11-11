from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField, URLField
from wtforms.validators import (DataRequired, Length, Optional, URL,
                                ValidationError)

from .constants import MAX_SHORT_LENGTH
from .utils import check_custom_id


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(require_tld=False, message='Здесь должен быть URL')
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(1, MAX_SHORT_LENGTH)]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        if not check_custom_id(field.data):
            raise ValidationError(
                'Ссылка должна состоять из латинских букв и цифр')
