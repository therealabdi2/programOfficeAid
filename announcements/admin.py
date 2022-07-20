from django.contrib import admin

# Register your models here.
from announcements.models import Announcement, Comment, SendSMS, AnnouncementSubscribers


class AnnouncementAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author",)
    list_display = ("title", "author", "created_at")
    readonly_fields = ("created_at", "updated_at")


class SendSMSAdmin(admin.ModelAdmin):
    model = SendSMS
    filter_horizontal = ('batch',)


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(AnnouncementSubscribers)
admin.site.register(SendSMS, SendSMSAdmin)
admin.site.register(Comment)
