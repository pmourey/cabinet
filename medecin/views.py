from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Consultation
from .forms import ConsultationForm, PatientForm

@login_required
def accueil(request):
    return render(request, 'medecin/accueil.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "medecin/login.html", {"error": "Identifiants invalides"})
    return render(request, "medecin/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, "medecin/patient_list.html", {"patients": patients})


@login_required
def consultation_list(request, patient_id=None):
    if patient_id:
        # Get consultations for a specific patient
        consultations = Consultation.objects.filter(patient_id=patient_id)
    else:
        # Get all consultations
        consultations = Consultation.objects.all()

    return render(request, "medecin/consultation_list.html", {"consultations": consultations, "patient_id": patient_id})


@login_required
def add_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.medecin = request.user
            consultation.save()
            return redirect('consultation_list')
    else:
        form = ConsultationForm()

    patients = Patient.objects.all()
    return render(request, 'medecin/consultation_form.html', {'form': form, 'patients': patients})


@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.medecin = request.user  # If you're tracking the creating doctor
            patient.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'medecin/patient_form.html', {'form': form})
