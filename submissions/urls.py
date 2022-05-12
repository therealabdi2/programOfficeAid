from django.contrib.auth.decorators import login_required
from django.urls import path

from submissions.views import JoiningFormView, JoiningDetailView

app_name = 'submissions'

urlpatterns = [
    path('joining_form/', login_required(JoiningFormView.as_view()), name='joining_form'),
    path('joining_detail/<int:pk>/', login_required(JoiningDetailView.as_view()), name='joining_detail'),
]