import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text = "Enter a date between now and 4 weeks (default 3).")

    # Used to validate a single field, overrides the method clean_<fieldname>()
    def clean_renewal_date(self):
        # Gets the data "cleaned" and converted to correct standard type
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past
        if data < datetime.date.today():
            # (_ ()) in case to translate the site later
            raise ValidationError(_('Invalid date - renewal in the past'))

        # Check if a date is in the allowed range (+4 weeks from today)
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data
        return data