from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from courses.models import Course, CourseType, CourseCategory, Session, OfferedCourses
from accounts.models import Programme


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


class CourseResource(resources.ModelResource):
    class Meta:
        model = Course


class CourseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = 'course_code', 'course_name', 'course_credit', 'prerequisite_display'
    list_filter = ['course_type', 'course_programme']
    filter_horizontal = ['course_programme']
    search_fields = ['course_code', 'course_name']
    search_help_text = 'Search by course code or course name'
    list_per_page = 10

    resource_class = CourseResource

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


class OfferedCoursesAdmin(admin.ModelAdmin):
    list_display = 'semester', 'offered_to', 'courses_offered'
    list_filter = ['semester', 'programme']
    search_fields = ['semester', 'programme']
    search_help_text = 'Search by semester or programme'
    list_per_page = 10
    filter_horizontal = ['course', 'programme']

    fieldsets = [
        (None, {'fields': ['semester']}),
        ('Select Programmes', {'fields': ['programme']}),
        ('Select Courses', {'fields': ['course']}),

    ]

    def offered_to(self, obj):
        return ", ".join([
            programme.degree_name for programme in obj.programme.all()
        ])

    def courses_offered(self, obj):
        return ", ".join([
            course.course_name for course in obj.course.all()
        ])


class SessionAdmin(admin.ModelAdmin):
    search_fields = ['session_name', 'session_year']
    search_help_text = 'Search by session name e.g SPR 2022'
    list_display = 'session_name', 'session_year', 'session_start_date', 'session_end_date'
    list_filter = ['session_name', 'session_year', ]
    list_per_page = 10


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(OfferedCourses, OfferedCoursesAdmin)
