<!-- TOC -->
    * [Ajout styling Bootstrap automatique](#ajout-styling-bootstrap-automatique)
    * [How to populate select lists automatically by Django through the form field definition](#how-to-populate-select-lists-automatically-by-django-through-the-form-field-definition)
    * [Responsive design activation](#responsive-design-activation)
    * [Validation - Renforcer la validation des données](#validation---renforcer-la-validation-des-données)
      * [Modèles (clean methods):](#modèles-clean-methods)
      * [Formulaires (clean_field methods):](#formulaires-clean_field-methods)
    * [Pagination - Ajouter pour les listes longues](#pagination---ajouter-pour-les-listes-longues)
    * [Recherche - Filtres sur patients/consultations](#recherche---filtres-sur-patientsconsultations)
    * [Export PDF des consultations](#export-pdf-des-consultations)
<!-- TOC -->

### Ajout styling Bootstrap automatique

J'ai modifié consultation_form.html pour utiliser widget_tweaks :

1. Ajouté `{% load widget_tweaks %}` en haut du template 
2. Remplacé tous les champs HTML manuels par les champs du formulaire Django avec |add_class 
3. Appliqué les classes Bootstrap appropriées (form-control, form-select)

Maintenant les deux formulaires utilisent widget_tweaks pour un styling Bootstrap cohérent et automatique.

### How to populate select lists automatically by Django through the form field definition


1. In the form (ConsultationForm):
    ```class ConsultationForm(forms.ModelForm):
        class Meta:
            model = Consultation
            fields = ['patient', 'date', 'motif', 'observations', 'prescription']
    ```
   
2. The patient field is a ForeignKey in the Consultation model:
    ```
    class Consultation(models.Model):
        patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    ```
   
3. Django automatically creates a ModelChoiceField for ForeignKey fields, which:
   * Queries all Patient objects: Patient.objects.all()
   * Uses the Patient model's __str__ method for display text 
   * Generates `<option value="patient.id">patient.__str__()</option>` for each patient


4. The Patient __str__ method provides the display text:
    ```
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    ```

### Responsive design activation

    <meta name="viewport" content="width=device-width, initial-scale=1">

Cette balise est essentielle pour que Bootstrap fonctionne correctement sur mobile. Elle indique au navigateur :

    - width=device-width : utiliser la largeur de l'écran de l'appareil
    - initial-scale=1 : ne pas zoomer par défaut


### Validation - Renforcer la validation des données

J'ai renforcé la validation des données avec :

#### Modèles (clean methods):

* Patient : Format téléphone, date naissance pas future, numéro sécurité sociale 15 chiffres 
* Consultation : Date pas future, motif min 3 caractères, observations obligatoires

#### Formulaires (clean_field methods):

* PatientForm : Nom/prénom lettres uniquement + capitalisation, téléphone format valide 
* ConsultationForm : Date pas future, motif min 3 caractères, observations obligatoires

Les validations s'appliquent automatiquement lors de `form.is_valid()` et affichent les erreurs dans les templates Bootstrap existants.

J'ai aussi modifié les vues pour afficher les erreurs de validation des modèles :

1. Ajouté `full_clean()` avant `save()` pour déclencher la validation du modèle 
2. Capturé les `ValidationError` et ajouté les erreurs au formulaire avec `form.add_error()`
3. Importé `ValidationError` dans les vues

Maintenant, quand une validation échoue au niveau du modèle (comme format téléphone, date future, etc.), l'erreur s'affiche dans le formulaire Bootstrap avec le styling existant.

### Pagination - Ajouter pour les listes longues

J'ai ajouté la pagination aux listes :

Vues :
* Importé Paginator de Django 
* Ajouté pagination avec 10 éléments par page 
* Remplacé les variables patients/consultations par page_obj

Templates :
* Mis à jour les boucles pour utiliser page_obj 
* Ajouté les contrôles de pagination Bootstrap avec liens Premier/Précédent/Suivant/Dernier 
* Affichage du numéro de page actuel

La pagination s'affiche automatiquement quand il y a plus de 10 éléments.

### Recherche - Filtres sur patients/consultations

J'ai ajouté la fonctionnalité de recherche :

Vues :

* Patients : recherche par nom ou prénom (icontains)
* Consultations : recherche par motif ou nom/prénom du patient

Templates :
* Formulaire de recherche avec champ de saisie 
* Bouton "Effacer" pour supprimer le filtre 
* Conservation de la valeur recherchée dans le champ

La recherche fonctionne avec la pagination et est insensible à la casse.

### Export PDF des consultations

J'ai ajouté l'export PDF des consultations :

Dépendance :
* Ajouté reportlab==4.0.4 dans requirements.txt

Vue :
* export_consultations_pdf() génère un PDF avec tableau des consultations 
* Support pour toutes les consultations ou celles d'un patient spécifique 
* Troncature du texte long pour l'affichage

URLs :
* /consultations/export/pdf/ - toutes les consultations 
* /consultations/<id>/export/pdf/ - consultations d'un patient

Template :
* Bouton "Export PDF" dans la liste des consultations 
* Téléchargement automatique du fichier PDF

Pour installer : pip install reportlab==4.0.4