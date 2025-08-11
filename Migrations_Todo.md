Pour mettre à jour le modèle de données après avoir modifié le champ email, vous devez :
1. Créer une migration :
    ```
    source .venv/bin/activate  # Activer l'environnement virtuel
    python manage.py makemigrations medecin
    ```
2. Appliquer la migration :
    ```
    python manage.py migrate
   ```
   
Les changements dans votre modèle :

* email = models.EmailField(blank=True, null=False) - permet email vide mais pas NULL 
* numero_securite_sociale = models.CharField(max_length=15, unique=False) - supprime la contrainte unique

Django créera automatiquement une migration pour ces modifications de champs.

Attention:

Le problème est que clean_email() n'est appelée que si le champ email a une valeur. Avec blank=True, Django ne valide pas les champs vides.

   ```
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError({'email': 'Format d\'email invalide'})
        
        return cleaned_data
   ```