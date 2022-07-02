from django.contrib.auth.decorators import login_required
from django.urls import path

from submissions.views import AllJoiningView, JoiningFormView, JoiningDetailView, JoiningCreateView, JoiningUpdateView, \
    OfferedCoursesView

app_name = 'submissions'

urlpatterns = [
    path('joining_form/', login_required(JoiningFormView.as_view()), name='joining_form'),
    path('update_joining/<int:pk>/', login_required(JoiningUpdateView.as_view()), name='update_joining'),
    path('all_joining/', login_required(AllJoiningView.as_view()), name='all_joining'),
    path('create_joining/', login_required(JoiningCreateView.as_view()), name='create_joining_form'),
    path('joining_detail/<int:pk>/', login_required(JoiningDetailView.as_view()), name='joining_detail'),
    path('offered_courses/<str:programme>/', login_required(OfferedCoursesView.as_view()),
         name='offered_courses'),
]
