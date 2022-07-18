from django.contrib.auth.decorators import login_required
from django.urls import path

from queries.views import QueryListView, QueryDetailView, LikeQueryView, LikeQueryCommentVIew, DeleteQueryCommentView, \
    CreateQueryView, UserQueryListView, DeleteQueryView

app_name = 'queryapp'

urlpatterns = [
    path('', QueryListView.as_view(), name='query_list'),
    path('student_queries/', login_required(UserQueryListView.as_view()), name='student_queries'),
    path('make_query/', login_required(CreateQueryView.as_view()), name='make_query'),
    path('delete-query/<slug:slug>/', login_required(DeleteQueryView.as_view()), name='delete_query'),
    path('<slug:slug>/', QueryDetailView.as_view(), name='query_detail'),
    path('like_query/<slug:slug>/', login_required(LikeQueryView.as_view()), name='like_query'),
    path('like_comment/<int:pk>/', login_required(LikeQueryCommentVIew.as_view()), name='like_query_comment'),
    path('delete_query_comment/<int:pk>/', login_required(DeleteQueryCommentView.as_view()),
         name='delete_query_comment'),

]
