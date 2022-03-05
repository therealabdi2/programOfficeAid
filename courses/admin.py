from django.contrib import admin

# Register your models here.
from courses.models import Course, CourseType, CourseCategory


class CourseInline(admin.TabularInline):
    model = Course
    extra = 0


class CourseTypeInline(admin.TabularInline):
    model = CourseType
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    list_display = 'course_code', 'course_name', 'course_credit'
    list_filter = 'course_type', 'course_programme'


class CourseTypeAdmin(admin.ModelAdmin):
    inlines = [CourseInline]


class CourseCategoryAdmin(admin.ModelAdmin):
    inlines = [CourseTypeInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseType, CourseTypeAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
