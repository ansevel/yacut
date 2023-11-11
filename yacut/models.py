from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), index=True, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            original=self.original,
            short=url_for(
                'redirect_to_original_link',
                short_id=self.short,
                _external=True
            )
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])
