from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from accounts.forms import StudentProfileForm
from accounts.models import Account, StudentProfile


class DashboardView(DetailView):
    model = StudentProfile
    template_name = 'accounts/dashboard.html'

    def get_object(self, *args, **kwargs):
        return StudentProfile.objects.get(student_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.get_object()
        return context


class CreateProfileView(View):
    def get(self, request):
        form = StudentProfileForm()
        context = {'form': form}
        return render(request, 'accounts/create_profile.html', context)

    def post(self, request):
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student_id = request.user.id
            profile = Account.objects.get(id=obj.student_id)
            profile.profile_completion = True
            profile.save()
            obj.save()
            return redirect('/accounts/dashboard/')
        context = {'form': form}
        return render(request, 'accounts/create_profile.html', context)


class EditProfileView(View):
    def get(self, request):
        student_profile = get_object_or_404(StudentProfile, student_id=request.user.id)
        form = StudentProfileForm(instance=student_profile)
        form.fields['registration_number'].disabled = True
        form.fields['faculty'].disabled = True
        form.fields['department'].disabled = True
        form.fields['programme'].disabled = True
        form.fields['batch'].disabled = True
        form.fields['section'].disabled = True
        context = {'form': form}
        return render(request, 'accounts/edit_profile.html', context)

    def post(self, request):
        POST = request.POST.copy()
        student_profile = get_object_or_404(StudentProfile, student_id=request.user.id)
        POST['registration_number'] = student_profile.registration_number
        POST['faculty'] = student_profile.faculty
        POST['department'] = student_profile.department
        POST['programme'] = student_profile.programme
        POST['batch'] = student_profile.batch
        POST['section'] = student_profile.section

        form = StudentProfileForm(POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:dashboard')

        context = {'form': form}
        return render(request, 'accounts/edit_profile.html', context)
