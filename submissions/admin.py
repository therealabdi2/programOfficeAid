from django import forms
from django.contrib import admin
# Register your models here.
from django.core.exceptions import ValidationError

from submissions.models import Joining


class JoiningForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Joining

    def clean(self):
        courses = self.cleaned_data.get('course')
        credit_hours = sum(courses.values_list('course_credit', flat=True))
        if credit_hours > 21:
            raise ValidationError(
                f'The max amount of credit hours allocated for this session is 21. '
                f'You have selected {credit_hours} credit hours.')


class JoiningAdmin(admin.ModelAdmin):
    form = JoiningForm
    list_display = ['session', 'get_reg_num', 'semester', 'form_status']
    filter_horizontal = ['course']
    list_filter = ['form_status', 'session__session_name', 'student__batch', 'semester', ]
    readonly_fields = ('session',)

    @admin.display(description='Student Reg Num')
    def get_reg_num(self, obj):
        return obj.student.registration_number


admin.site.register(Joining, JoiningAdmin)
