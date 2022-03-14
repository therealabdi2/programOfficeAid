from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from accounts.forms import RegisterForm


class RegisterView(View):
    def get(self, request):
        context = {"form": RegisterForm()}
        return render(request, 'accounts/register.html', context=context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponse('HI')
        context = {"form": form}
        return render(request, 'accounts/register.html', context=context)
