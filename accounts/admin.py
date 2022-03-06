from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from accounts.models import Account, Batch, Faculty, Department, Programme, Section, StudentProfile


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'username',
        'last_login',
        'date_joined',
        'is_active',
    )
    list_display_links = ('email', 'first_name', 'last_name',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class StudentAdmin(admin.ModelAdmin):
    search_help_text = 'Search by student Registration Number, first name, last name, or email'
    list_display = 'student_full_name', 'registration_number', 'faculty', 'programme', 'batch', 'section', 'department',
    search_fields = ['registration_number', 'student__first_name', 'student__last_name', 'student__email']
    list_filter = ['batch', 'programme', 'section', 'department', 'faculty']
    list_per_page = 10
    readonly_fields = ["profile_picture_image"]

    def profile_picture_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.profile_picture.url,
            width=obj.profile_picture.width,
            height=obj.profile_picture.height,
        )
        )

    @display(description='Name')
    def student_full_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"


class StudentInline(admin.TabularInline):
    model = StudentProfile
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    list_display = 'section_name', 'batch'
    list_display_links = ('section_name', 'batch',)
    search_fields = ['section_name', 'batch__batch_name']
    inlines = [StudentInline]
    list_per_page = 10


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    show_change_link = True


class BatchAdmin(admin.ModelAdmin):
    inlines = [SectionInline]
    list_per_page = 10


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    show_change_link = True


class ProgrammeInline(admin.TabularInline):
    model = Programme
    extra = 0
    show_change_link = True


class BatchInline(admin.TabularInline):
    model = Batch
    extra = 0
    show_change_link = True


class DepartmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['department_name']}),
        ('Faculty information', {'fields': ['faculty']}),
    ]
    inlines = [ProgrammeInline]


class FacultyAdmin(admin.ModelAdmin):
    inlines = [DepartmentInline]

    def has_delete_permission(self, request, obj=None):
        return False


class ProgrammeAdmin(admin.ModelAdmin):
    list_display = 'degree_name', 'department'
    fieldsets = [
        (None, {'fields': ['degree_name']}),
        ('Department information', {'fields': ['department']}),
    ]
    inlines = [BatchInline]


admin.site.register(Account, AccountAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(StudentProfile, StudentAdmin)
