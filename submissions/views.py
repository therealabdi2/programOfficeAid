from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView

from submissions.models import Joining


class JoiningFormView(ListView):
    model = Joining
    template_name = 'submissions/joining.html'

