from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io

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
	patients = Patient.objects.filter(medecin=request.user)
	
	# Search functionality
	search = request.GET.get('search')
	if search:
		patients = patients.filter(
			nom__icontains=search
		) | patients.filter(
			prenom__icontains=search
		)
	
	paginator = Paginator(patients, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, "medecin/patient_list.html", {"page_obj": page_obj, "search": search})


@login_required
@group_required(['medecin', 'admin'])
def consultation_list(request, patient_id=None):
	if patient_id:
		# Get consultations for a specific patient belonging to the doctor
		consultations = Consultation.objects.filter(patient_id=patient_id, patient__medecin=request.user)
	else:
		# Get all consultations for patients belonging to the doctor
		consultations = Consultation.objects.filter(patient__medecin=request.user)

	# Search functionality
	search = request.GET.get('search')
	if search:
		consultations = consultations.filter(
			motif__icontains=search
		) | consultations.filter(
			patient__nom__icontains=search
		) | consultations.filter(
			patient__prenom__icontains=search
		)

	paginator = Paginator(consultations, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, "medecin/consultation_list.html", {"page_obj": page_obj, "patient_id": patient_id, "search": search})


@login_required
@group_required(['medecin', 'admin'])
def add_consultation(request):
	form = ConsultationForm(request.POST or None, user=request.user)
	if form.is_valid():
		consultation = form.save(commit=False)
		try:
			consultation.full_clean()
			consultation.save()
			return redirect('medecin:patient_list')
		except ValidationError as e:
			for field, errors in e.message_dict.items():
				for error in errors:
					form.add_error(field, error)

	return render(request, 'medecin/consultation_form.html', {'form': form})


@login_required
@group_required(['medecin', 'admin'])
def add_patient(request):
	form = PatientForm(request.POST or None)
	if form.is_valid():
		patient = form.save(commit=False)
		patient.medecin = request.user
		try:
			patient.full_clean()
			patient.save()
			return redirect('medecin:patient_list')
		except ValidationError as e:
			for field, errors in e.message_dict.items():
				for error in errors:
					form.add_error(field, error)

	return render(request, 'medecin/patient_form.html', {'form': form})


@login_required
@group_required(['medecin', 'admin'])
def export_consultations_pdf(request, patient_id=None):
	if patient_id:
		consultations = Consultation.objects.filter(patient_id=patient_id, patient__medecin=request.user)
		filename = f"consultations_patient_{patient_id}.pdf"
	else:
		consultations = Consultation.objects.filter(patient__medecin=request.user)
		filename = "toutes_consultations.pdf"
	
	buffer = io.BytesIO()
	doc = SimpleDocTemplate(buffer, pagesize=A4)
	styles = getSampleStyleSheet()
	elements = []
	
	# Title
	title = Paragraph("Rapport de Consultations", styles['Title'])
	elements.append(title)
	elements.append(Spacer(1, 12))
	
	# Table data
	data = [['Date', 'Patient', 'Motif', 'Observations']]
	for consultation in consultations:
		data.append([
			consultation.date.strftime('%d/%m/%Y'),
			str(consultation.patient),
			consultation.motif[:30] + '...' if len(consultation.motif) > 30 else consultation.motif,
			consultation.observations[:40] + '...' if len(consultation.observations) > 40 else consultation.observations
		])
	
	# Create table
	table = Table(data)
	table.setStyle(TableStyle([
		('BACKGROUND', (0, 0), (-1, 0), colors.grey),
		('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
		('ALIGN', (0, 0), (-1, -1), 'CENTER'),
		('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
		('FONTSIZE', (0, 0), (-1, 0), 14),
		('BOTTOMPADDING', (0, 0), (-1, 0), 12),
		('BACKGROUND', (0, 1), (-1, -1), colors.beige),
		('GRID', (0, 0), (-1, -1), 1, colors.black)
	]))
	
	elements.append(table)
	doc.build(elements)
	
	buffer.seek(0)
	response = HttpResponse(buffer, content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename="{filename}"'
	return response
