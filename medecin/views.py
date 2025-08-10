from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from cabinet.decorators import group_required
from .models import Patient, Consultation
from .forms import ConsultationForm, PatientForm


@login_required
@group_required(['medecin', 'admin'])
def accueil(request):
	return render(request, 'medecin/accueil.html')


@login_required
@group_required(['medecin', 'admin'])
def patient_list(request):
	patients = Patient.objects.all()
	return render(request, "medecin/patient_list.html", {"patients": patients})


@login_required
@group_required(['medecin', 'admin'])
def consultation_list(request, patient_id=None):
	if patient_id:
		# Get consultations for a specific patient
		consultations = Consultation.objects.filter(patient_id=patient_id)
	else:
		# Get all consultations
		consultations = Consultation.objects.all()

	return render(request, "medecin/consultation_list.html", {"consultations": consultations, "patient_id": patient_id})


@login_required
@group_required(['medecin', 'admin'])
def add_consultation(request):
	form = ConsultationForm(request.POST or None)
	if form.is_valid():
		consultation = form.save(commit=False)
		consultation.medecin = request.user
		consultation.save()
		return redirect('medecin:patient_list')

	return render(request, 'medecin/consultation_form.html', {'form': form})


@login_required
@group_required(['medecin', 'admin'])
def add_patient(request):
	form = PatientForm(request.POST or None)
	if form.is_valid():
		patient = form.save(commit=False)
		patient.medecin = request.user
		patient.save()
		return redirect('medecin:patient_list')

	return render(request, 'medecin/patient_form.html', {'form': form})
