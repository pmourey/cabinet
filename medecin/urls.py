from django.urls import path, include
from . import views

app_name = 'medecin'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    # path('accounts/', include('django.contrib.auth.urls')),  # moved to cabinet.urls
    path('patients/', views.patient_list, name='patient_list'),
    path('consultation/add/', views.add_consultation, name='add_consultation'),
    path('patients/add/', views.add_patient, name='add_patient'),
    # URL for all consultations
    path('consultations/', views.consultation_list, name='consultations'),
    # URL for patient-specific consultations
    path('consultations/<int:patient_id>/', views.consultation_list, name='consultations_patient'),
]

