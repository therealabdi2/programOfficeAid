from django.contrib import admin

# Register your models here.
from submissions.models import JoiningForm


class JoiningFormAdmin(admin.ModelAdmin):
    list_display = ['session', 'get_reg_num', 'semester', 'form_status']
    filter_horizontal = ['course']
    list_filter = ['form_status', 'session__session_name', 'session__batch', 'semester', ]

    @admin.display(description='Student Reg Num')
    def get_reg_num(self, obj):
        return obj.student.registration_number


admin.site.register(JoiningForm, JoiningFormAdmin)
