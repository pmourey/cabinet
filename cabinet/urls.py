from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='medecin').exists():
            return redirect('/medecin/')  # Use direct path instead of named URL
        elif request.user.groups.filter(name='strava').exists():
            return redirect('/strava/')   # Use direct path instead of named URL
    return redirect('/accounts/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('medecin.urls', namespace='medecin')),
    path('strava/', include('strava.urls', namespace='strava')),
    # path('', root_redirect, name='root'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]
