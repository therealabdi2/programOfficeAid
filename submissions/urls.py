from django.contrib.auth.decorators import login_required
from django.urls import path

from submissions.views import JoiningFormView, JoiningDetailView, JoiningCreateView

app_name = 'submissions'

urlpatterns = [
    path('joining_form/', login_required(JoiningFormView.as_view()), name='joining_form'),
    path('create_joining/', login_required(JoiningCreateView.as_view()), name='create_joining_form'),
    path('joining_detail/<int:pk>/', login_required(JoiningDetailView.as_view()), name='joining_detail'),
]