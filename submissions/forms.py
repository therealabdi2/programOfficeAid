from ajax_select.fields import AutoCompleteSelectMultipleField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from courses.models import Course
from submissions.models import Joining, AddDropForm


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


class StudentAddDropForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentAddDropForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['add_course'].required = False
        self.fields['drop_course'].required = False

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = AddDropForm
        fields = ['semester', 'add_course', 'drop_course', 'fee_slip',]

    add_course = AutoCompleteSelectMultipleField('courses',
                                                 help_text='Type in the course name,'
                                                           'Click the red button to remove the course',
                                                 label='Select Courses to add', )

    drop_course = AutoCompleteSelectMultipleField('courses',
                                                  help_text='Type in the course name'
                                                            'Click the red button to remove the course',
                                                  label='Select Courses to drop')

    def clean(self):
        add_courses = self.cleaned_data.get('add_course')
        drop_courses = self.cleaned_data.get('drop_course')
        if not add_courses and not drop_courses:
            raise ValidationError('Add or drop at least one course')

        total_credits_hours = 0
        if add_courses:
            for c in add_courses:
                course = Course.objects.get(pk=c)
                total_credits_hours += course.course_credit

        if total_credits_hours > 21:
            raise ValidationError(
                f'The max amount of credit hours allocated for this session is 21. '
                f'You have selected {total_credits_hours} credit hours.')
