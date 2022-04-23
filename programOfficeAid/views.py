# display the homepage
from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'home/about.html')


class ServicesView(View):
    def get(self, request):
        return render(request, 'home/services.html')
