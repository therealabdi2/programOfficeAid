from django.contrib import admin

# Register your models here.
from queries.models import QueryPost, QueryComment

admin.site.register(QueryPost)
admin.site.register(QueryComment)