from django.contrib import admin

# Register your models here.
from queries.models import QueryPost, QueryComment, StudentFeedback


class QueryPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author",)
    list_display = ("title", "author", "created_at")


class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ("user",)
    list_display = ("user", "text", "timestamp")


admin.site.register(QueryPost, QueryPostAdmin)
admin.site.register(QueryComment)
admin.site.register(StudentFeedback, FeedbackAdmin)
