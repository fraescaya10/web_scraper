## How to run this application

1. Install pipenv `pip3 install pipenv`.
2. Run `pipenv shell`.
3. Once the virtualenv is working run `pipenv install` to install the dependencies.
4. In order to have the database with the necessary table run `python build_db.py`.
5. Finally run `python app.py` to have the flask application up.

## How to test the endpoints
There are three endpoints `GET /scrape`, `GET /employees`, `GET /managers`, the first one is used to scrape the whiteoaksf website and save the information in the database, the other ones are to get a list of employes or managers respectively.