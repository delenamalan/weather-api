from django import forms
from django.core.exceptions import ValidationError
from datetime import date, datetime
import re
from django.utils.translation import gettext_lazy as _, ngettext_lazy

DATE_FORMAT = "%Y/%m/%d"

class DatePeriodField(forms.CharField):
    default_error_messages = {
        'invalid': _('Must have the format: yyyy/mm/dd-yyyy/mm/dd.'),
    }

    def clean(self, value):
        cleaned = super().clean(value)

        # Convert period to dates
        regex = r'(\d{4}/\d{2}/\d{2})-(\d{4}/\d{2}/\d{2})'
        match = re.match(regex, cleaned)
        if not match:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
    
        try: 
            start = datetime.strptime(match.group(1), DATE_FORMAT).date()
            end = datetime.strptime(match.group(2), DATE_FORMAT).date()
        except ValueError:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
            
        return start, end


class WeatherForm(forms.Form):
    city = forms.RegexField(r'^(\w|-| )+$', error_messages={'invalid':"City may only contain alphabetical characters, spaces and hypens"}, max_length=100)
    period = DatePeriodField()