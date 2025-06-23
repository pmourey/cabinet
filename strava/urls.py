from django.urls import path, include
from . import views

app_name = 'strava'

urlpatterns = [
	# path('', views.accueil, name='accueil'),
	# path('', views.index, name='index'),
	path('activities/', views.activity_list, name='activity_list'),
	# path('oauth/', include('social_django.urls', namespace='social')),
	path('', views.base_map, name='Base Map View'),
	path('connected/', views.connected_map, name='Connect Map View'),
	path("oauth/", include("social_django.urls", namespace="social")),
	# path('social-auth/', include('social_django.urls', namespace='social')),
]
