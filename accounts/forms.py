from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from django import forms


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
