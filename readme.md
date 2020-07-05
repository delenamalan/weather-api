# Weather API

## Setup instructions

### API

Dependencies:
- Python 3.6
- SQLite (or change the settings to use a different database)

```
cd api
virtualenv -p /usr/bin/python3.6 venv && source venv/bin/activate
pip install -r requirements.txt
cd weathersite
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend


## Routes
