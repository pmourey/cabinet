from django import forms
from .models import Consultation, Patient

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


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'date_naissance', 'sexe', 'adresse',
                 'telephone', 'email', 'numero_securite_sociale']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
        }
