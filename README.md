# Mongolit
Simple school project build in [Python](https://www.python.org/)-[Flask](https://flask.palletsprojects.com/en/2.3.x/) 
with [Bootstrap v5](https://getbootstrap.com/) and [MongoDB](https://mongodb.com/)

## What you need
- [Python](https://www.python.org/)
- Dependency management [poetry](https://python-poetry.org/)
- Create [Mongo](https://mongodb.com/) account
- Configurate `.env` file based on `env.example`

## Run project
### On Unix systems (Linux, macOS)
- `python -m venv venv`
- `poetry install && poetry update`
- `python configure_database.py`
- `export FLASK_APP=mongolit/app.py`
- `flask run`


If you want export `requirements.txt` run: 
- `poetry export -f requirements.txt --output requirements.txt --without-hashes`


## Users
All users have the same password: `password123`

---
With ❤️️ and ☕️ Erik Belák (c) 2023
