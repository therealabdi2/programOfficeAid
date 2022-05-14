from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import ModelForm

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

    def clean(self):
        courses = self.cleaned_data.get('course')
        credit_hours = sum(courses.values_list('course_credit', flat=True))
        if credit_hours > 21:
            raise ValidationError(
                f'The max amount of credit hours allocated for this session is 21. '
                f'You have selected {credit_hours} credit hours.')
