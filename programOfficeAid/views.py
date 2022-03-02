# display the homepage
from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
