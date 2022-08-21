from django.contrib.auth.decorators import login_required
from django.urls import path
from accounts.api.apiviews import UserViewSet
from .views import DashboardView, CreateProfileView, EditProfileView

from rest_framework.routers import SimpleRouter

app_name = 'accounts'

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
urlpatterns = router.urls

urlpatterns += [

    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),
    path('create_profile/', login_required(CreateProfileView.as_view()), name='create_profile'),
    path('edit_profile/', login_required(EditProfileView.as_view()), name='edit_profile'),
]
