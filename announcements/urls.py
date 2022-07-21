from django.contrib.auth.decorators import login_required
from django.urls import path

from announcements.views import AnnouncementSubscriptionView, AllAnnouncementsView, AnnouncementDetailView, \
    DeleteCommentView, LikeAnnouncementView, \
    LikeCommentVIew, SavedAnnouncementView

app_name = 'announcements'

urlpatterns = [
    path('all_announcements/', AllAnnouncementsView.as_view(), name='all_announcements'),
    path('announcement_detail/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('subscribe-annoucements/', login_required(AnnouncementSubscriptionView.as_view()),
         name='subscribe_announcements'),
    path('like/<int:pk>/', login_required(LikeAnnouncementView.as_view()), name='like_post'),
    path('like_comment/<int:pk>/', login_required(LikeCommentVIew.as_view()), name='like_comment'),
    path('delete_comment/<int:pk>/', login_required(DeleteCommentView.as_view()), name='delete_comment'),
    path('saved_announcements/', login_required(SavedAnnouncementView.as_view()), name='saved_announcements'),
]
