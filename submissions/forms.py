from ajax_select.fields import AutoCompleteSelectMultipleField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from courses.models import Course
from submissions.models import Joining


class StudentJoiningForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentJoiningForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.disable_csrf = True

    class Meta:
        model = Joining
        fields = ['semester', 'course', 'fee_slip']

    course = AutoCompleteSelectMultipleField('courses',
                                             help_text='Type in the course name e.g <strong>'
                                                       'Introduction to Computing</strong>, '
                                                       'Click the red button to remove the course',
                                             plugin_options={'autoFocus': True},
                                             required=True, label='Select Courses')

    def clean(self):
        courses = self.cleaned_data.get('course')
        if not courses:
            raise ValidationError('Submit at least one course')

        total_credits_hours = 0
        for c in courses:
            course = Course.objects.get(pk=c)
            total_credits_hours += course.course_credit

        if total_credits_hours > 21:
            raise ValidationError(
                f'The max amount of credit hours allocated for this session is 21. '
                f'You have selected {total_credits_hours} credit hours.')

        # credit_hours = sum(courses.values_list('course_credit', flat=True))
        # if credit_hours > 21:
        #     raise ValidationError(
        #         f'The max amount of credit hours allocated for this session is 21. '
        #         f'You have selected {credit_hours} credit hours.')
