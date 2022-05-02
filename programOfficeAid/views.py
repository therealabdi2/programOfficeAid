# display the homepage
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


class AboutView(TemplateView):
    template_name = 'home/about.html'


class ServicesView(TemplateView):
    template_name = 'home/services.html'
