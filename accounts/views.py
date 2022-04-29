from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import StudentProfileForm
from accounts.models import Account


class DashboardView(View):
    def get(self, request):
        return render(request, 'accounts/dashboard.html')


class CreateProfileView(View):
    def get(self, request):
        print(request.user.profile_completion)
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
