import logging
from datetime import datetime
from . import db

log = logging.getLogger(__name__)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(100))
    company = db.Column(db.String(30))
    city = db.Column(db.String(100))
    division = db.Column(db.String(100))
    department = db.Column(db.String(100))
    type = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.role = kwargs['role']
        self.company = kwargs['company']
        self.city = kwargs['city']
        self.division = kwargs['division']
        self.department = kwargs['department']
        self.type = kwargs['type']

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()
