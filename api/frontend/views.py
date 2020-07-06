from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from api.forms import WeatherForm


class WeatherView(FormView):
    template_name = "weather_form.html"
    form_class = WeatherForm
    success_url = "/weather-result"

    def form_valid(self, form):
        return super().form_valid(form)


class WeatherResultView(TemplateView):
    template_name = "weather_result.html"

    def get_context_data(self, **kwargs):
        # Do an AJAX request
        context = super().get_context_data(**kwargs)
        return context
