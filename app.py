from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from scraper import WhiteoaksfScraper


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


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


class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'role', 'company', 'city',
                  'division', 'department', 'type')


member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


@app.route('/scrape', methods=['GET'])
def scrape_whiteoaksf():
    scraper = WhiteoaksfScraper(
        'https://whiteoaksf.com/leadership-and-professionals/')
    scraped_members = scraper.scrap_managers() + scraper.scrap_employees()
    print('There are {} scraped members'.format(len(scraped_members)))
    try:
        for scraped_member in scraped_members:
            member = Member(**scraped_member)
            db.session.add(member)
            db.session.commit()
    except Exception as e:
        db.session.rollback()

    members_saved = Member.query.all()
    print('There are {} members saved'.format(len(members_saved)))
    result = members_schema.dump(members_saved)
    return jsonify(result)


@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Member.query.filter_by(type='employee')
    result = members_schema.dump(employees)
    print('There are {} employees saved'.format(len(result)))
    return jsonify(result)


@app.route('/managers', methods=['GET'])
def get_managers():
    managers = Member.query.filter_by(type='manager')
    result = members_schema.dump(managers)
    print('There are {} managers saved'.format(len(result)))
    return jsonify(result)


if __name__ == "__main__":
    app.run()
