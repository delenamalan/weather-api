from django.urls import include, path

from . import views

urlpatterns = [
    # path("/weather", include(views.weather)),
    path("weather", views.weather),
]
