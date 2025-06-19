from django.urls import path
from . import views

app_name = 'strava'

urlpatterns = [
	path('', views.accueil, name='accueil'),
	path('activities/', views.activity_list, name='activity_list')
]
