from django.contrib.auth.decorators import login_required
from django.urls import path

from queries.views import QueryListView, QueryDetailView, LikeQueryView, LikeQueryCommentVIew, DeleteQueryCommentView

app_name = 'queryapp'

urlpatterns = [
    path('', QueryListView.as_view(), name='query_list'),
    path('<int:pk>/', QueryDetailView.as_view(), name='query_detail'),
    path('like_query/<int:pk>/', login_required(LikeQueryView.as_view()), name='like_query'),
    path('like_comment/<int:pk>/', login_required(LikeQueryCommentVIew.as_view()), name='like_query_comment'),
    path('delete_query_comment/<int:pk>/', login_required(DeleteQueryCommentView.as_view()),
         name='delete_query_comment'),

]
