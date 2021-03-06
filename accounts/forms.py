from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm

from accounts.models import StudentProfile


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'type': 'email',
            'class': 'form-control',
            'placeholder': "Email Address",
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': "Password"
        })


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.fields['first_name'].widget = forms.TextInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': "First Name",
        })
        self.fields['last_name'].widget = forms.PasswordInput(attrs={
            'type': 'text',
            'class': 'form-control',
            'placeholder': "Last Name"
        })
        self.fields['email'].widget = forms.TextInput(attrs={
            'type': 'email',
            'class': 'form-control',
            'placeholder': "Email Address",
        })
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': "Password"
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'type': 'password',
            'class': 'form-control',
            'placeholder': "Password (again)"
        })

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class StudentProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.disable_csrf = True

    class Meta:
        model = StudentProfile
        exclude = ['student']
        labels = {
            'fatherName': 'Parent/Guardian Name',
        }
