# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Exclude certain paths from redirection
            excluded_paths = ['/admin/', '/accounts/', '/medecin/', '/strava/', '/']
            if not any(request.path.startswith(path) for path in excluded_paths):
                try:
                    if request.user.groups.filter(name='medecin').exists():
                        return redirect(reverse('medecin:accueil'))
                    elif request.user.groups.filter(name='strava').exists():
                        return redirect(reverse('strava:accueil'))
                except:
                    pass

        response = self.get_response(request)
        return response
