from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from imagekit.admin import AdminThumbnail

from accounts.models import Account, Batch, Faculty, Department, Programme, Section, StudentProfile
from submissions.admin import JoiningForm
from submissions.models import Joining


# Register your models here.


class BatchInline(admin.TabularInline):
    model = Batch
    extra = 0
    show_change_link = True


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    show_change_link = True


class ProgrammeInline(admin.TabularInline):
    model = Programme
    extra = 0
    show_change_link = True


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    show_change_link = True


class StudentInline(admin.TabularInline):
    model = StudentProfile
    extra = 1


class JoiningFormInline(admin.StackedInline):
    model = Joining
    form = JoiningForm
    extra = 0
    filter_horizontal = ('course',)
    show_change_link = True


class AccountAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password', 'profile_completion')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser',
                                    'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('user_permissions',)
    search_fields = ('email', 'first_name', 'last_name')

    list_display = (
        'email',
        'first_name',
        'last_name',
        'last_login',
        'date_joined',
        'is_active',
    )
    list_display_links = ('email', 'first_name', 'last_name',)
    list_filter = ()
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('email',)


class BatchAdmin(admin.ModelAdmin):
    autocomplete_fields = ['programme']
    inlines = [SectionInline]
    list_per_page = 10
    search_fields = ['batch_name']
    search_help_text = 'Search by batch name'


class DepartmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['faculty']
    fieldsets = [
        (None, {'fields': ['department_name']}),
        ('Faculty information', {'fields': ['faculty']}),
    ]
    inlines = [ProgrammeInline]
    search_fields = ['department_name']
    search_help_text = 'Search by department name'


class FacultyAdmin(admin.ModelAdmin):
    inlines = [DepartmentInline]
    search_fields = ['faculty_name']
    search_help_text = 'Search by faculty name'


class ProgrammeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['department']
    fieldsets = [
        (None, {'fields': ['degree_name']}),
        ('Department information', {'fields': ['department']}),
    ]
    inlines = [BatchInline]
    list_display = 'degree_name', 'department'
    search_fields = ['degree_name']
    search_help_text = 'Search by degree name'


class SectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['batch']
    inlines = [StudentInline]
    list_display = 'section_name', 'batch'
    list_per_page = 10
    search_fields = ['section_name']
    search_help_text = 'Search by section or batch name'


class StudentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['faculty', 'programme', 'batch', 'section', 'department']
    list_display = (
        'student_full_name', 'registration_number', 'faculty', 'programme', 'batch', 'section', 'department',)
    list_filter = ['batch', 'programme', 'section', 'department', 'faculty']
    list_per_page = 10
    search_fields = ['registration_number', 'student__first_name', 'student__last_name', 'student__email']
    search_help_text = 'Search by student Registration Number, first name, last name, or email'
    readonly_fields = ["profile_picture_image"]
    inlines = [JoiningFormInline]

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


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(StudentProfile, StudentAdmin)
