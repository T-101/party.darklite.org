from dal import autocomplete

from django import forms

from authentication.models import User


class UsersForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'display_name': autocomplete.Select2(url='dal-users')
        }
