import logging
from flask import jsonify
from . import app
from .schemas import MemberSchema
from .models import Member
from .scraper import WhiteoaksfScraper

log = logging.getLogger(__name__)

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


@app.route('/api/scrape', methods=['GET'])
def scrape_whiteoaksf():
    scraper = WhiteoaksfScraper()
    scraped_members = scraper.scrap_members()
    log.info('There are {} scraped members'.format(len(scraped_members)))

    for scraped_member in scraped_members:
        member = Member(**scraped_member)
        member.save()

    members_saved = Member.query.all()
    log.info('There are {} members saved'.format(len(members_saved)))
    result = members_schema.dump(members_saved)
    return jsonify(result)


@app.route('/api/members', methods=['GET'])
def get_all_members():
    members = Member.query.all()
    result = members_schema.dump(members)
    log.info('There are {} members saved'.format(len(result)))
    return jsonify(result)


@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Member.query.filter_by(type='employee')
    result = members_schema.dump(employees)
    log.info('There are {} employees saved'.format(len(result)))
    return jsonify(result)


@app.route('/api/managers', methods=['GET'])
def get_managers():
    managers = Member.query.filter_by(type='manager')
    result = members_schema.dump(managers)
    log.info('There are {} managers saved'.format(len(result)))
    return jsonify(result)
