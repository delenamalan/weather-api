from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from datetime import date
from importlib import import_module
from django.conf import settings
from api.forms import WeatherForm


def get_weather_instance_from_weather_settings(weather_import):
    last_dot = weather_import.rfind(".")
    weather_module = weather_import[:last_dot]
    weather_class_name = weather_import[last_dot + 1 :]
    module = import_module(weather_module)
    weather_class = getattr(module, weather_class_name)
    return weather_class()


weather_import = (
    settings.WEATHER_CLASS
    if settings.WEATHER_CLASS
    else "weather.metaweather.MetaWeather"
)
weather_instance = get_weather_instance_from_weather_settings(weather_import)


def weather(request):
    if request.method == "GET":
        form = WeatherForm(request.GET)
        if not form.is_valid():
            return JsonResponse(form.errors.get_json_data(), status=400)

        city = form.cleaned_data["city"]
        period_start, period_end = form.cleaned_data["period"]
        result = weather_instance.query(city, period_start, period_end)
        return JsonResponse(result.to_dict())
    else:
        return HttpResponseNotFound()
