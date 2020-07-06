from django.urls import include, path

from . import views

urlpatterns = [
    path("weather", views.WeatherView.as_view()),
    path("weather-result", views.WeatherResultView.as_view()),
]
