from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import ParentForm, JoiningForm


# Register your models here.
class ParentFormChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = ParentForm  # Optional, explicitly set here.


class JoiningFormAdmin(ParentFormChildAdmin):
    list_display = ['session', 'get_reg_num', 'semester', 'form_status']
    base_model = JoiningForm
    filter_horizontal = ['course']
    list_filter = ['form_status', 'session__session_name', 'session__batch', 'semester', ]
    readonly_fields = ['student', 'submitted_at', 'semester', 'session',]

    @admin.display(description='Student Reg Num')
    def get_reg_num(self, obj):
        return obj.student.registration_number


class ParentFormAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = ParentForm
    child_models = (JoiningForm,)


# admin.site.register(ParentForm, ParentFormAdmin)
admin.site.register(JoiningForm, JoiningFormAdmin)
