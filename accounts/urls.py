from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import DashboardView, CreateProfileView

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),
    path('create_profile/', login_required(CreateProfileView.as_view()), name='create_profile'),
]
