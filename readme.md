# Django Weather API

I used the [MetaWeather API](https://www.metaweather.com/api/) to fetch weather data. It can fetch historical weather data as well as up to a five day forecast.

I created an abstract base class to fetch weather so that it can easily be replaced by a different provider or a mock. Replace the `WEATHER_CLASS` settings value with `"api.tests.mock_weather.MockWeather"` to use a mock weather class instead.

Files of note:
 - [`weather` module](api/weather/weather.py) that contains the abstract base class, `Weather`, and other useful classes.
 - [`metaweather` module](./api/weather/metaweather.py) that contains the MetaWeather specific code.
 - [Tests](api/weather/tests/test_metaweather.py) for weather fetching code.
 - [View class](api/api/views.py).
 - [View test](api/api/tests/test_api.py).
 - [Forms tests](api/api/tests/test_forms.py).

## Setup instructions

### API

System requirements:

- Python 3.6
- Virtualenv
- Pip

Installation:

```
cd api
virtualenv -p /usr/bin/python3.6 venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Django might warn you to run migrations, but there's no need to set up a database or run migrations because we're not currently storing anything in a database.

Fetching results:

```
curl 'http://127.0.0.1:8000/api/weather?city=cape%20town&period=2020/07/01-2020/07/02'
```

Viewing results in a browser:

[http://127.0.0.1:8000/weather](http://127.0.0.1:8000/weather)

Running the tests:

```
python manage.py test
```

## Formatting files

We use Black to format files:

```
cd api
source venv/bin/activate
black --exclude ./venv/ ./
```
