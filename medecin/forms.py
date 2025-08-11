from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Consultation, Patient
import re

class ConsultationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['patient'].queryset = Patient.objects.filter(medecin=user)
    
    class Meta:
        model = Consultation
        fields = ['patient', 'date', 'motif', 'observations', 'prescription']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'observations': forms.Textarea(attrs={'rows': 4}),
            'prescription': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise ValidationError('La date de consultation ne peut pas être dans le futur')
        return date
    
    def clean_motif(self):
        motif = self.cleaned_data.get('motif')
        if motif and len(motif.strip()) < 3:
            raise ValidationError('Le motif doit contenir au moins 3 caractères')
        return motif.strip()
    
    def clean_observations(self):
        observations = self.cleaned_data.get('observations')
        if not observations or not observations.strip():
            raise ValidationError('Les observations sont obligatoires')
        return observations.strip()


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'date_naissance', 'sexe', 'adresse',
                 'telephone', 'email', 'numero_securite_sociale']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not re.match(r'^[a-zA-ZÀ-ſ\s\-\']+$', nom):
            raise ValidationError('Le nom ne doit contenir que des lettres, espaces, tirets et apostrophes')
        return nom.title()
    
    def clean_prenom(self):
        prenom = self.cleaned_data.get('prenom')
        if not re.match(r'^[a-zA-ZÀ-ſ\s\-\']+$', prenom):
            raise ValidationError('Le prénom ne doit contenir que des lettres, espaces, tirets et apostrophes')
        return prenom.title()
    
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not re.match(r'^[0-9+\-\s\.\(\)]+$', telephone):
            raise ValidationError('Format de téléphone invalide')
        return telephone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Format d\'email invalide')
        return email
