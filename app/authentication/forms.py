from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from django.contrib.auth import get_user_model
from django.forms import ModelForm


class DisplayNameForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'display_name'
            ),
            ButtonHolder(
                Submit('submit', 'Change')
            )
        )

    class Meta:
        model = get_user_model()
        fields = ['display_name']
        help_texts = {
            "display_name": "This is the default display name that will be written to a new trip. "
                            "Changing this will not affect previous trips."
        }
