from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin'), ('A', 'Autre'), ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    numero_securite_sociale = models.CharField(max_length=15, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    medecin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Consultation(models.Model):
    date = models.DateField()  # Remove auto_now or auto_now_add if present
    motif = models.CharField(max_length=200)
    observations = models.TextField()
    prescription = models.TextField(blank=True)

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.patient} - {self.date}"
