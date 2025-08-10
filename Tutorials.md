### J'ai modifié consultation_form.html pour utiliser widget_tweaks :

1. Ajouté `{% load widget_tweaks %}` en haut du template 
2. Remplacé tous les champs HTML manuels par les champs du formulaire Django avec |add_class 
3. Appliqué les classes Bootstrap appropriées (form-control, form-select)

Maintenant les deux formulaires utilisent widget_tweaks pour un styling Bootstrap cohérent et automatique.

### The select list is populated automatically by Django through the form field definition. Here's how it works:

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
    ```
    <meta name="viewport" content="width=device-width, initial-scale=1">
    ```

Cette balise est essentielle pour que Bootstrap fonctionne correctement sur mobile. Elle indique au navigateur :

    - width=device-width : utiliser la largeur de l'écran de l'appareil
    - initial-scale=1 : ne pas zoomer par défaut

