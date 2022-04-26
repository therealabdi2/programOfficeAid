from django.http import HttpResponseRedirect
from django.urls import reverse


class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        user = request.user
        if user.is_authenticated:
            if not user.profile_completion:
                while not (request.path == reverse('accounts:create_profile')):
                    return HttpResponseRedirect(reverse('accounts:create_profile'))

        return response

