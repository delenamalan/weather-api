from django.urls import include, path

from . import views

urlpatterns = [
    path("weather", views.WeatherView.as_view(), name="api.weather"),
]
