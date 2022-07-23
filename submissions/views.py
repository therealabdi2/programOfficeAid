# Create your views here.
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from accounts.models import StudentProfile
from courses.models import Session, OfferedCourses, Course
from submissions.forms import StudentAddDropForm, StudentJoiningForm
from submissions.models import Joining, AddDropForm


class AddDropFormView(ListView):
    model = AddDropForm
    template_name = 'submissions/add_drop_form_list.html'
    context_object_name = 'add_drop_forms'
    paginate_by = 5

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, student_id=self.request.user.id)
        return self.model.objects.filter(student=profile).order_by('-id')[:3]


class AddDropFormDetailView(DetailView):
    model = AddDropForm
    template_name = 'submissions/add_drop_form_detail.html'
    context_object_name = 'add_drop_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_courses'] = self.object.add_course.all()
        context['drop_courses'] = self.object.drop_course.all()
        return context


class AddDropFormCreateView(CreateView):
    model = AddDropForm
    form_class = StudentAddDropForm
    template_name = 'submissions/add_drop_form_create.html'

    def form_valid(self, form):
        form.instance.student = StudentProfile.objects.get(student_id=self.request.user.id)
        form.instance.save()
        messages.success(self.request, 'Form submitted successfully.')
        return super().form_valid(form)

    session_deadline = Session.objects.latest('session_start_date').is_deadline()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['session_deadline'] = self.session_deadline
        return context

    def get_success_url(self):
        return reverse('submissions:add_drop_form_list')


class AddDropFormUpdateView(UpdateView):
    model = AddDropForm
    form_class = StudentAddDropForm
    template_name = 'submissions/add_drop_form_update.html'
    context_object_name = 'add_drop_form'

    def form_valid(self, form):
        # check status of the joining object
        if self.object.form_status != 'Pending':
            messages.error(self.request,
                           f'You cannot update this form as it has already been {self.object.form_status},'
                           f' by Program Office Staff')
            return redirect('submissions:joining_form')
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Your form has been updated.')
        return reverse('submissions:add_drop_form_list')


class JoiningFormView(ListView):
    model = Joining
    session_deadline = Session.objects.latest('session_start_date').is_deadline()
    template_name = 'submissions/joining.html'
    context_object_name = 'joiningforms'

    # give session in context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['session_deadline'] = self.session_deadline
        return context

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, student_id=self.request.user.id)
        return self.model.objects.filter(student=profile).order_by('-id')[:3]


class AllJoiningView(ListView):
    paginate_by = 10
    model = Joining
    template_name = 'submissions/all_joining.html'
    context_object_name = 'joiningforms'

    def get_queryset(self):
        profile = get_object_or_404(StudentProfile, student_id=self.request.user.id)
        return self.model.objects.filter(student=profile).order_by('-id')


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
        student_joining_form = StudentJoiningForm()
        session_deadline = Session.objects.latest('session_start_date').is_deadline()

        context = {'form': student_joining_form,
                   'session_deadline': session_deadline
                   }
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


class JoiningUpdateView(UpdateView):
    model = Joining
    form_class = StudentJoiningForm
    template_name = "submissions/update_joining.html"
    context_object_name = 'joining'

    def form_valid(self, form):
        # check status of the joining object
        if self.object.form_status != 'Pending':
            messages.error(self.request,
                           f'You cannot update this form as it has already been {self.object.form_status},'
                           f' by Program Office Staff')
            return redirect('submissions:joining_form')
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Your form has been updated.')
        return reverse("submissions:joining_form")


# get courses offered in semester for a specific programme
class OfferedCoursesView(View):
    def get(self, request, programme):
        semester = request.GET.get('semester')
        # prefetch the courses names offered in the semester
        offered_courses = OfferedCourses.objects.filter(semester=semester, programme__degree_name=programme). \
            prefetch_related('course').values_list('course__course_code',
                                                   'course__course_name',
                                                   'course__course_prerequisite__course_name')

        previous_courses = Joining.objects.filter(student__student_id=request.user.id,
                                                  form_status='Accepted'). \
            prefetch_related('course').values_list('course__course_code',
                                                   'course__course_name', )
        context = {
            'offered_courses': offered_courses,
            'previous_courses': previous_courses,
        }
        return render(request, 'submissions/offered_courses.html', context)
