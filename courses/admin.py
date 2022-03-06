from django.contrib import admin

# Register your models here.
from courses.models import Course, CourseType, CourseCategory, Session


class CourseInline(admin.TabularInline):
    model = Course
    fields = ['course_code', 'course_credit']
    readonly_fields = ['course_code', 'course_credit']
    show_change_link = True
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


class CourseTypeInline(admin.TabularInline):
    model = CourseType
    readonly_fields = ['course_type_name']
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


class CourseAdmin(admin.ModelAdmin):
    list_display = 'course_code', 'course_name', 'course_credit', 'prerequisite_display'
    list_filter = ['course_type', 'course_programme']
    ordering = ['course_code']
    search_fields = ['course_code', 'course_name']
    search_help_text = 'Search by course code or course name'
    list_per_page = 10

    def prerequisite_display(self, obj):
        return ", ".join([
            prerequisite_course.course_name for prerequisite_course in obj.prerequisite_course.all()
        ])

    prerequisite_display.short_description = "Prerequisite of"


class CourseTypeAdmin(admin.ModelAdmin):
    list_display = 'course_type_name', 'course_type_category'
    list_filter = ['course_type_category']
    inlines = [CourseInline]


class CourseCategoryAdmin(admin.ModelAdmin):
    inlines = [CourseTypeInline]


class SessionAdmin(admin.ModelAdmin):
    filter_horizontal = ('courses_offered',)
    search_fields = ['session_name']
    search_help_text = 'Search by session name e.g SPR-2022'
    list_display = 'session_name', 'batch', 'session_start_date', 'session_end_date'
    list_filter = ['session_start_date', 'batch']
    list_per_page = 10


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Session, SessionAdmin)
