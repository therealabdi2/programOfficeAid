from django.contrib import admin

# Register your models here.
from announcements.models import Announcement, Comment


class AnnouncementAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author",)
    list_display = ("title", "author", "created_at")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Comment)
