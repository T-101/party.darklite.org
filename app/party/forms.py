from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder

from common.classes import LocaleDateTimePicker, LocaleDatePicker
from party.models import Party, Trip


class PartyForm(forms.ModelForm):
    date_start = forms.DateField(widget=LocaleDatePicker(attrs={"type": "date", "append": "fas fa-calendar"}))
    date_end = forms.DateField(widget=LocaleDatePicker(attrs={"type": "date", "append": "fas fa-calendar"}))

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


class TripForm(forms.ModelForm):
    departure_country = forms.CharField(widget=autocomplete.ListSelect2(url='dal-countries'))
    arrival_country = forms.CharField(widget=autocomplete.ListSelect2(url='dal-countries'))

    departure_datetime = forms.DateTimeField(
        widget=LocaleDateTimePicker(attrs={"class": "col-md-12", "append": "fas fa-calendar"}))
    arrival_datetime = forms.DateTimeField(
        widget=LocaleDateTimePicker(attrs={"class": "col-md-12", "append": "fas fa-calendar"}))
    towards_home = forms.BooleanField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        is_required = kwargs.pop("is_required", False)
        towards_home = kwargs.pop("towards_home", False)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Do not render <form> tags for each FormClass
        for field in ["departure_town", "arrival_town", "departure_datetime",
                      "arrival_datetime", "departure_country", "arrival_country"]:
            setattr(self.fields[field], "required", is_required)
        self.fields["towards_home"].required = towards_home

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
                Column('type', css_class="col-md-3"),
                Column('detail1', css_class="col-md-4"),
                Column('detail2', css_class="col-md-4"),
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )

    class Meta:
        model = Trip
        exclude = ['party', 'created_by', 'display_name']
        help_texts = {
            "detail1": "Optional. Can be airline, car make, whatever",
            "detail2": "Optional. Can be flight number, car registration plate, whatever"
        }


class TripFormNative(TripForm):
    departure_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    arrival_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))


class PartyFormNative(PartyForm):
    date_start = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    date_end = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
