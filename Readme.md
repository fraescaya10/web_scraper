## How to run this application

1. Install pipenv `pip3 install pipenv`.
2. Run `pipenv shell`.
3. Once the virtualenv is working run `pipenv install` to install the dependencies.
4. In order to have the database with the necessary table run `python build_db.py`.
5. Finally run `python run.py` to have the flask application up.

## How to test the endpoints
There are four endpoints `GET /api/scrape`, `GET /api/members`,,`GET /api/employees`, `GET /api/managers`, the first one is used to scrape the whiteoaksf website and save the information in the database, the other ones are to get a list of members, employes and managers respectively.