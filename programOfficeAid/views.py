
# display the homepage
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')
