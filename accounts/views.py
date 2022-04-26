from django.shortcuts import render
from django.views import View


class DashboardView(View):
    def get(self, request):
        return render(request, 'accounts/dashboard.html')


class CreateProfileView(View):
    def get(self, request):
        return render(request, 'accounts/create_profile.html')
