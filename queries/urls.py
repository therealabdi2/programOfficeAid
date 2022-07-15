from django.urls import path

from queries.views import QueryListView

app_name = 'queryapp'

urlpatterns = [
    path('', QueryListView.as_view(), name='query_list'),
]
