from django.shortcuts import render
from .common import get_activities
from datetime import timedelta

# Create your views here.

def accueil(request):
	return render(request, 'strava/accueil.html')

def activity_list(request):
	# activity_filter = 'running' # ['running', 'cycling', 'walking']
	activities = get_activities()
	# activities = list(filter(lambda x: x[6] == activity_filter, activities))
	total_distance = sum(activity[1] for activity in activities)
	elapsed_time = timedelta(seconds=sum(activity[2] for activity in activities))
	average_speed = total_distance / elapsed_time.total_seconds() * 3600
	return render(request, "strava/activity_list.html", {"activities": activities, "total_distance": total_distance, "elapsed_time": elapsed_time, "average_speed": average_speed, "activity_filter": activity_filter})
