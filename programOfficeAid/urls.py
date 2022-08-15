from ajax_select import urls as ajax_select_urls
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from programOfficeAid.views import AboutView, HomeView, ServicesView
from queries.views import StudentFeedbackView

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('contact/', StudentFeedbackView.as_view(), name='feedback'),

    path('api-auth/', include('rest_framework.urls')),
    path("api/v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    path("api/v1/dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),

    path('accounts/', include('allauth.urls')),

    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    path('announcements/', include(('announcements.urls', 'announcements'), namespace='announcements')),

    path('queries/', include(('queries.urls', 'queries'), namespace='queries')),

    path('submissions/', include(('submissions.urls', 'submissions'), namespace='submissions')),

    path('timetable/', include(('timetable.urls', 'timetable'), namespace='timetable')),

    path(r'^ajax_select/', include(ajax_select_urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
