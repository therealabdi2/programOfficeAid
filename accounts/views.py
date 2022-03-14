from django.shortcuts import render
from django.views import View

from accounts.forms import RegisterForm


class RegisterView(View):
    def get(self, request):
        context = {"form": RegisterForm()}
        return render(request, 'accounts/register.html', context=context)
