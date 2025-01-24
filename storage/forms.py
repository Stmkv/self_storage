from django import forms
from django.core.exceptions import ValidationError


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.TextInput(
            attrs={"class": "form-control datepicker", "placeholder": "Дата начала"}
        ),
        label="Дата начала",
    )
    end_date = forms.DateField(
        widget=forms.TextInput(
            attrs={"class": "form-control datepicker", "placeholder": "Дата конца"}
        ),
        label="Дата конца",
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите адрес"}
        ),
        label="Адрес",
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise ValidationError("Дата начала не может быть позже даты конца.")
