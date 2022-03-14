from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Account


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

        first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
        email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'password')
