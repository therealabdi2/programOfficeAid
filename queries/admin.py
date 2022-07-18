from django.contrib import admin

# Register your models here.
from queries.models import QueryPost, QueryComment


class QueryPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author",)
    list_display = ("title", "author", "created_at")



admin.site.register(QueryPost, QueryPostAdmin)
admin.site.register(QueryComment)
