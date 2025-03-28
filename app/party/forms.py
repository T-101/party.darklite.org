from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django_countries import countries

from common.classes import LocaleDateTimePicker, LocaleDatePicker
from party.models import Party, Trip


class CustomSelect(forms.Select):

    def __init__(self, *args, **kwargs):
        disabled_options: list = kwargs.pop("disabled_options", [])
        super().__init__()
        self.disabled_options = disabled_options

    def optgroups(self, name, value, attrs=None):
        groups = super().optgroups(name, value, attrs)
        if groups and self.disabled_options:
            for option in self.disabled_options:
                try:
                    groups[option][1][0]["attrs"]["disabled"] = True
                except IndexError:
                    pass
        return groups


class PartyForm(forms.ModelForm):
    date_start = forms.DateField(widget=LocaleDatePicker())
    date_end = forms.DateField(widget=LocaleDatePicker())
    country = autocomplete.Select2ListChoiceField(widget=autocomplete.ListSelect2(url='dal-countries'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields["country"].initial = self.instance.country
        self.fields["country"].choices = list(countries)

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
                Column('location', css_class="col-md-6"),
                Column('country', css_class="col-md-6 mb-2")
            ),
            Row(
                Column(
                    Submit('submit', 'Save'),
                    HTML("""<a role="button" class="btn btn-outline-primary ms-4"
                        href="{% url "party:landing_page" %}">Cancel</a>""")
                )
            )
        )

    class Meta:
        model = Party
        exclude = ['slug', 'created_by', 'modified_by']


def _trip_layout():
    return Layout(
        Row(
            Column('display_name', css_class="col-md-4"),
        ),
        Row(
            Column('departure_town', css_class="col-md-4"),
            Column('departure_country', css_class="col-md-4"),
            Column('departure_datetime', css_class="col-md-4 col-lg-3")
        ),
        Row(
            Column('arrival_town', css_class="col-md-4"),
            Column('arrival_country', css_class="col-md-4"),
            Column('arrival_datetime', css_class="col-md-4 col-lg-3"),
        ),
        Row(
            Column('type', css_class="col-md-4"),
            Column('detail1', css_class="col-md-4"),
            Column('detail2', css_class="col-md-4"),
        ),
    )


class TripForm(forms.ModelForm):
    departure_country = autocomplete.Select2ListChoiceField(widget=autocomplete.ListSelect2(url='dal-countries'))
    arrival_country = autocomplete.Select2ListChoiceField(widget=autocomplete.ListSelect2(url='dal-countries'))
    type = forms.ChoiceField(choices=[(None, "Select one")] + Trip.TYPES,
                             widget=CustomSelect(attrs={'class': 'form-control form-select'}, disabled_options=[0]))

    departure_datetime = forms.DateTimeField(
        widget=LocaleDateTimePicker(attrs={"class": "col-md-12", "append": "fas fa-calendar"}))
    arrival_datetime = forms.DateTimeField(
        widget=LocaleDateTimePicker(attrs={"class": "col-md-12", "append": "fas fa-calendar"}))
    towards_party = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        is_required = kwargs.pop("is_required", False)
        display_name = kwargs.pop("display_name", None)
        trip_instance = kwargs.pop("trip_instance", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Do not render <form> tags for each FormClass
        for field in ["display_name", "departure_town", "arrival_town", "departure_datetime",
                      "arrival_datetime", "departure_country", "arrival_country"]:
            setattr(self.fields[field], "required", is_required)
        self.fields["towards_party"].required = False
        if display_name is not None:
            self.fields["display_name"].initial = display_name

        if trip_instance is not None:
            trip = trip_instance
        else:
            trip = self.instance
        self.fields["departure_country"].initial = trip.departure_country
        self.fields["departure_country"].choices = list(countries)
        self.fields["arrival_country"].initial = trip.arrival_country
        self.fields["arrival_country"].choices = list(countries)

        self.helper.layout = _trip_layout()

    class Meta:
        model = Trip
        exclude = ['party', 'created_by']
        help_texts = {
            "display_name": "You can change this default value by clicking your name in the nav bar",
            "detail1": "Optional. Can be airline, car make, whatever",
            "detail2": "Optional. Can be flight number, car registration plate, whatever"
        }


class TripFormNative(TripForm):
    departure_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    arrival_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    type = forms.ChoiceField(choices=Trip.TYPES)


class PartyFormNative(PartyForm):
    date_start = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    date_end = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
