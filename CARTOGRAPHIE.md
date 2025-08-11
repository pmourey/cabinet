# Cartographie de l'Application Cabinet Médical

## Architecture Générale

```
cabinet/
├── cabinet/          # Configuration Django
├── medecin/          # Application principale
├── templates/        # Templates globaux
└── scripts/          # Scripts utilitaires
```

## URLs et Navigation

### URLs Principales
- `/` → Accueil (medecin:accueil)
- `/accounts/login/` → Connexion Django
- `/patients/` → Liste des patients
- `/patients/add/` → Nouveau patient
- `/consultation/add/` → Nouvelle consultation
- `/consultations/` → Toutes les consultations
- `/consultations/<id>/` → Consultations d'un patient

### Flux de Navigation
```
Connexion → Accueil → [Patients/Consultations]
                  ↓
            [Ajouter Patient/Consultation]
```

## Modèles de Données

### Patient
- nom, prenom, date_naissance, sexe
- adresse, telephone, email
- numero_securite_sociale (unique)
- medecin (ForeignKey vers User)

### Consultation
- date, motif, observations, prescription
- patient (ForeignKey vers Patient)

## Vues et Fonctionnalités

### Vues Principales
1. **accueil** - Dashboard principal
2. **patient_list** - Liste des patients
3. **add_patient** - Formulaire nouveau patient
4. **consultation_list** - Liste des consultations
5. **add_consultation** - Formulaire nouvelle consultation

### Sécurité
- Authentification requise (@login_required)
- Autorisation par groupe (@group_required(['medecin', 'admin']))

## Templates et Interface

### Structure des Templates
```
base.html (Bootstrap 5.3)
├── accueil.html (Dashboard avec cards)
├── patient_list.html (Table Bootstrap)
├── patient_form.html (Formulaire avec validation)
├── consultation_list.html (Table responsive)
└── consultation_form.html (Formulaire complet)
```

### Composants Bootstrap
- Cards pour les sections
- Tables responsives
- Formulaires stylisés
- Alertes pour les erreurs
- Boutons avec classes appropriées

## Formulaires

### PatientForm
- Tous les champs Patient sauf medecin
- Widget date pour date_naissance
- Textarea pour adresse

### ConsultationForm
- Tous les champs Consultation
- Widget date pour date
- Textareas pour observations/prescription

## Sécurité et Permissions

### Décorateur group_required
- Vérifie l'appartenance aux groupes 'medecin' ou 'admin'
- Lève PermissionDenied si non autorisé

### Authentification
- Django auth system
- Templates de connexion personnalisés
- Redirection après connexion

## Points d'Amélioration Identifiés

- [x] **Formulaires** - Ajouter widget_tweaks pour styling Bootstrap
- [x] **Validation** - Renforcer la validation des données
- [x] **Pagination** - Ajouter pour les listes longues
- [x] **Recherche** - Filtres sur patients/consultations
- [ ] **Export** - PDF des consultations