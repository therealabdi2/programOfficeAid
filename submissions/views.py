# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from accounts.models import StudentProfile
from submissions.models import Joining


class JoiningFormView(ListView):
    model = Joining
    template_name = 'submissions/joining.html'
    context_object_name = 'joiningforms'

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, student_id=self.request.user.id)
        return self.model.objects.filter(student=profile).order_by('-id')[:3]
