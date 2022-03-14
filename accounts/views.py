from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

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
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
