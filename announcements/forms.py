from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Textarea
from django import forms

from announcements.models import Comment


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Post your comment',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 5}),
        }
