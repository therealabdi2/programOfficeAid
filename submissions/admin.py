from django import forms
from django.contrib import admin
# Register your models here.
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from submissions.models import Joining, AddDropForm, Petition


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
    readonly_fields = ('session', 'fee_slip_image')

    @admin.display(description='Student Reg Num')
    def get_reg_num(self, obj):
        return obj.student.registration_number

    def fee_slip_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.fee_slip.url,
            width=obj.fee_slip.width,
            height=obj.fee_slip.height,
        )
        )


class AddDropFormAdmin(admin.ModelAdmin):
    filter_horizontal = ['add_course', 'drop_course']
    list_display = ['session', 'get_reg_num', 'semester', 'form_status']
    list_filter = ['form_status', 'session__session_name', 'student__batch', 'semester', ]
    readonly_fields = ('session', 'fee_slip_image')

    @admin.display(description='Student Reg Num')
    def get_reg_num(self, obj):
        return obj.student.registration_number

    def fee_slip_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.fee_slip.url,
            width=obj.fee_slip.width,
            height=obj.fee_slip.height,
        )
        )


class PetitionAdmin(admin.ModelAdmin):
    list_display = ['petition_title', 'form_status']
    list_filter = ['form_status', 'session__session_name', 'student__batch', 'semester', ]


admin.site.register(AddDropForm, AddDropFormAdmin)
admin.site.register(Joining, JoiningAdmin)
admin.site.register(Petition, PetitionAdmin)
