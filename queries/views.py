from django.shortcuts import render

from django.views.generic import ListView

from queries.models import QueryPost


class QueryListView(ListView):
    paginate_by = 5
    model = QueryPost
    context_object_name = 'queries'
    template_name = 'queries/query_list.html'
    ordering = ['-created_at']
