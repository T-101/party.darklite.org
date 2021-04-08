from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Hidden, Div, Row, Column, Field, Reset
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from common.classes import LocaleDateTimePicker
from party.models import Party, Trip, Airport


class PartyForm(forms.ModelForm):
    date_start = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    date_end = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('www')
            ),
            Row(
                Column('date_start'),
                Column('date_end')
            ),
            Row(
                Column('location'),
                Column('country')
            ),
            Row(
                Column(
                    Submit('submit', 'Save'),
                    Submit('cancel', 'Cancel')
                )
            )
        )

    class Meta:
        model = Party
        exclude = ['slug', 'created_by']


class FlightForm(forms.ModelForm):
    departure_country = forms.CharField(widget=autocomplete.ListSelect2(url='dal-countries'))
    arrival_country = forms.CharField(widget=autocomplete.ListSelect2(url='dal-countries'))

    departure_datetime = forms.DateTimeField(widget=LocaleDateTimePicker(attrs={"class": "col-md-12"}))
    arrival_datetime = forms.DateTimeField(widget=LocaleDateTimePicker(attrs={"class": "col-md-12"}))
    towards_home = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        is_required = kwargs.pop("is_required", False)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Do not render <form> tags for each FormClass
        for field in ["departure_town", "arrival_town",
                      "departure_datetime", "arrival_datetime",
                      "departure_country", "arrival_country"]:
            setattr(self.fields[field], "required", is_required)
        self.fields["towards_home"].required = False

        # self.fields["departure_country"].selected = ("PIER", "PIER")

        self.helper.layout = Layout(
            Row(
                Column('departure_town', css_class="col-md-4"),
                Column('departure_country', css_class="col-md-4"),
                Column('departure_datetime', css_class="col-md-3")
            ),
            Row(
                Column('arrival_town', css_class="col-md-4"),
                Column('arrival_country', css_class="col-md-4"),
                Column('arrival_datetime', css_class="col-md-3"),
            ),
            Row(
                Column('detail1', css_class="col-md-4"),
                Column('detail2', css_class="col-md-4"),
            ),
            # Row(
            #     Column(
            #         Submit('submit', 'Save'),
            #         Reset('reset', 'Cancel')
            #     )
            # )
        )

    class Meta:
        model = Trip
        exclude = ['party', 'handle', 'created_by', 'type']


class TripFormNative(FlightForm):
    departure_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    arrival_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))


class TravelForm(forms.ModelForm):
    departure_datetime = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    arrival_datetime = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column('type', css_class="col-sm-6"),
            ),
            Row(
                Column('departure_town', css_class="col-sm-3"),
                Column('departure_datetime', css_class="col-sm-3"),
            ),
            Row(
                Column('arrival_town', css_class="col-sm-3"),
                Column('arrival_datetime', css_class="col-sm-3")
            ),
            Row(
                Column('detail1', css_class="col-sm-3"),
                Column('detail2', css_class="col-sm-3")
            ),
            Row(
                Column(
                    Submit('submit', 'Save'),
                    Reset('reset', 'Cancel')
                )
            )
        )

    class Meta:
        model = Trip
        exclude = ['party', 'handle', 'towards_home', 'created_by']
