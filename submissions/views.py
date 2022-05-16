# Create your views here.
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from accounts.models import StudentProfile
from submissions.forms import StudentJoiningForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_courses = self.get_object().course.all()
        total_credits = total_courses.aggregate(total_credits=Sum('course_credit'))['total_credits']
        context['total_credits'] = total_credits
        return context


class JoiningCreateView(View):
    def get(self, request):
        form = StudentJoiningForm()
        context = {'form': form}
        return render(request, 'submissions/create_joining_form.html', context)

    def post(self, request):
        form = StudentJoiningForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            profile = get_object_or_404(StudentProfile, student_id=self.request.user.id)
            obj.student = profile
            obj.save()
            form.save()
            return redirect('submissions:joining_form')
        else:
            return render(request, 'submissions/create_joining_form.html', {'form': form})
