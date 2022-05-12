# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from accounts.models import StudentProfile
from submissions.models import Joining


class JoiningFormView(ListView):
    model = Joining
    template_name = 'submissions/joining.html'
    context_object_name = 'joiningforms'

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, student_id=self.request.user.id)
        return self.model.objects.filter(student=profile).order_by('-id')[:3]


class JoiningDetailView(DetailView):
    model = Joining
    template_name = 'submissions/joining_detail.html'
    context_object_name = 'joiningform'

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, student_id=self.request.user.id)
        return Joining.objects.filter(student=profile)

