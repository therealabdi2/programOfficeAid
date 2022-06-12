from django.contrib.auth.decorators import login_required
from django.urls import path

from announcements.views import AllAnnouncementsView, AnnouncementDetailView, DeleteCommentView, LikeAnnouncementView, \
    LikeCommentVIew

app_name = 'announcements'

urlpatterns = [
    path('all_announcements/', AllAnnouncementsView.as_view(), name='all_announcements'),
    path('announcement_detail/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('like/<int:pk>/', login_required(LikeAnnouncementView.as_view()), name='like_post'),
    path('like_comment/<int:pk>/', login_required(LikeCommentVIew.as_view()), name='like_comment'),
    path('delete_comment/<int:pk>/', login_required(DeleteCommentView.as_view()), name='delete_comment')
]
