from django.test import TestCase, Client, override_settings
from django.core.exceptions import ValidationError
from datetime import date
from django.urls import reverse
from api.forms import DatePeriodField, WeatherForm


class DatePeriodFieldTest(TestCase):
    def setUp(self):
        self.field = DatePeriodField()

    def test_date_period_field(self):
        self.assertEqual(
            (date(2020, 1, 1), date(2020, 2, 10)),
            self.field.clean("2020/01/01-2020/02/10"),
        )
        with self.assertRaises(ValidationError):
            self.field.clean("test value")
        with self.assertRaises(ValidationError):
            self.field.clean("2021/01/01-2020/02/10")
        with self.assertRaises(ValidationError):
            self.field.clean("")


class WeatherFormTest(TestCase):
    def test_valid_form(self):
        form = WeatherForm({"city": "cape town", "period": "2020/01/01-2020/02/10"})
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["city"], "cape town")
        self.assertEqual(
            form.cleaned_data["period"], (date(2020, 1, 1), date(2020, 2, 10))
        )

    def test_invalid_form(self):
        form = WeatherForm({"city": "not$&a city", "period": "not a period"})
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)
