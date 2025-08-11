from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class Patient(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin'), ('A', 'Autre'), ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    email = models.EmailField(null=False)
    numero_securite_sociale = models.CharField(max_length=15, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    medecin = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        # Validate email format
        if self.email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValidationError({'email': 'Format d\'email invalide'})

        # Validate phone number format
        if self.telephone and not re.match(r'^[0-9+\-\s\.\(\)]+$', self.telephone):
            raise ValidationError({'telephone': 'Format de téléphone invalide'})
        
        # Validate birth date not in future
        if self.date_naissance and self.date_naissance > timezone.now().date():
            raise ValidationError({'date_naissance': 'La date de naissance ne peut pas être dans le futur'})
        
        # Validate security number format (15 digits)
        if self.numero_securite_sociale and not re.match(r'^[0-9]{15}$', self.numero_securite_sociale):
            raise ValidationError({'numero_securite_sociale': 'Le numéro de sécurité sociale doit contenir exactement 15 chiffres'})

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Consultation(models.Model):
    date = models.DateField()  # Remove auto_now or auto_now_add if present
    motif = models.CharField(max_length=200)
    observations = models.TextField()
    prescription = models.TextField(blank=True)

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)


    def clean(self):
        # Validate consultation date not in future
        if self.date and self.date > timezone.now().date():
            raise ValidationError({'date': 'La date de consultation ne peut pas être dans le futur'})
        
        # Validate motif length
        if self.motif and len(self.motif.strip()) < 3:
            raise ValidationError({'motif': 'Le motif doit contenir au moins 3 caractères'})
        
        # Validate observations not empty
        if self.observations and not self.observations.strip():
            raise ValidationError({'observations': 'Les observations sont obligatoires'})

    def __str__(self):
        return f"{self.patient} - {self.date}"
