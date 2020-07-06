from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from datetime import date
from importlib import import_module
from django.conf import settings
from api.forms import WeatherForm
from django.views import View
from weather.metaweather import (
    NoWeatherForDayFoundException,
    NoManyWoeidFound,
    TooManyWoeidsFound,
)


def get_weather_instance_from_weather_settings(weather_import):
    last_dot = weather_import.rfind(".")
    weather_module = weather_import[:last_dot]
    weather_class_name = weather_import[last_dot + 1 :]
    module = import_module(weather_module)
    weather_class = getattr(module, weather_class_name)
    return weather_class()


class WeatherView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        weather_import = (
            settings.WEATHER_CLASS
            if settings.WEATHER_CLASS
            else "weather.metaweather.MetaWeather"
        )
        self.weather_instance = get_weather_instance_from_weather_settings(
            weather_import
        )

    def get(self, request):
        form = WeatherForm(request.GET)
        if not form.is_valid():
            return JsonResponse(form.errors.get_json_data(), status=400)

        city = form.cleaned_data["city"]
        period_start, period_end = form.cleaned_data["period"]
        try:
            result = self.weather_instance.query(city, period_start, period_end)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

        return JsonResponse(result.to_dict())
