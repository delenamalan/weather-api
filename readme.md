# Weather API

## Setup instructions

### API

Dependencies:
- Python 3.6
- SQLite (or change the settings to use a different database)

```
cd api
touch db.sqlite3
virtualenv -p /usr/bin/python3.6 venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

curl -H 'Accept: application/json; indent=4' -u <username>:<password> http://127.0.0.1:8000/api/users/

```

### Frontend


## Routes

## Formatting files

We use Black to format files:

```
cd api
source venv/bin/activate
black --exclude ./venv/ ./
```
