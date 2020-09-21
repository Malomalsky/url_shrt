from datetime import datetime
import string 
from .extensions import db, ma
from random import choices
import re 
from flask import jsonify


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(5), unique=True)
    custom_url = db.Column(db.String(100), default=None, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=5))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()
        return short_url

class LinkSchema(ma.Schema):
    class Meta:
        fields = ('id', 'original_url', 'short_url', 'custom_url', 'date_created')


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv