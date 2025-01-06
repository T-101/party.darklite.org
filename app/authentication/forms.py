from django.contrib.auth import get_user_model
from django.forms import ModelForm, CharField, TextInput


class DisplayNameForm(ModelForm):
    display_name = CharField(
        label="Your name",
        widget=TextInput(attrs={"placeholder": "Your name", "class": "form-control", "data-1p-ignore": "true"}),
        help_text="This is the default display name that will be written to a new trip. "
                  "Changing this will not affect previous trips."
    )

    class Meta:
        model = get_user_model()
        fields = ['display_name']
