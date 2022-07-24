from django.contrib.auth.decorators import login_required
from django.urls import path

from submissions.views import AddDropFormView, AddDropFormDetailView, AllJoiningView, JoiningFormView, \
    JoiningDetailView, JoiningCreateView, \
    JoiningUpdateView, \
    OfferedCoursesView, AddDropFormCreateView, AddDropFormUpdateView, PetitionListView, PetitionDetailView, \
    SignPetitionView, PetitionCreateView

app_name = 'submissions'

urlpatterns = [
    path('joining_form/', login_required(JoiningFormView.as_view()), name='joining_form'),
    path('update_joining/<int:pk>/', login_required(JoiningUpdateView.as_view()), name='update_joining'),
    path('all_joining/', login_required(AllJoiningView.as_view()), name='all_joining'),
    path('create_joining/', login_required(JoiningCreateView.as_view()), name='create_joining_form'),
    path('joining_detail/<int:pk>/', login_required(JoiningDetailView.as_view()), name='joining_detail'),
    path('offered_courses/<str:programme>/', login_required(OfferedCoursesView.as_view()),
         name='offered_courses'),

    path('add-drop-form-list/', login_required(AddDropFormView.as_view()), name='add_drop_form_list'),
    path('add-drop-form-detail/<int:pk>', login_required(AddDropFormDetailView.as_view()), name='add_drop_form_detail'),
    path('add-drop-form-create/', login_required(AddDropFormCreateView.as_view()), name='add_drop_form_create'),
    path('add-drop-form-update/<int:pk>', login_required(AddDropFormUpdateView.as_view()), name='add_drop_form_update'),

    path('petition-list/', login_required(PetitionListView.as_view()), name='petition_list'),
    path('petition-detail/<int:pk>', login_required(PetitionDetailView.as_view()), name='petition_detail'),
    path('petition-create/', login_required(PetitionCreateView.as_view()), name='petition_create'),
    path('sign-petition/<int:pk>', login_required(SignPetitionView.as_view()), name='sign_petition'),
]
