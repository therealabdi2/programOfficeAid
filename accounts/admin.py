from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from accounts.models import Account, Batch, Faculty, Department, Programme, Section, StudentProfile


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
    list_display = 'user', 'registration_number', 'batch', 'programme', 'section', 'department', 'faculty'
    search_fields = ['registration_number', 'user__first_name', 'user__last_name', 'user__username']


class StudentInline(admin.TabularInline):
    model = StudentProfile
    extra = 1


class SectionAdmin(admin.ModelAdmin):
    list_display = 'section_name', 'batch'
    inlines = [StudentInline]


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1


class FacultyAdmin(admin.ModelAdmin):
    inlines = [DepartmentInline]


admin.site.register(Account, AccountAdmin)
admin.site.register(Batch)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department)
admin.site.register(Programme)
admin.site.register(Section, SectionAdmin)
admin.site.register(StudentProfile, StudentAdmin)
