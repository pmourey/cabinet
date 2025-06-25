# Medical Office Management System

A Django web application for managing medical office operations, utilizing Django's built-in authentication system for secure access control.

## Features

- User authentication and authorization (Django's built-in auth system)
- Patient management
- Consultation tracking
- Secure access control for medical staff
- Admin interface for system management

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Create new virtual environment:
```bash
python3 -m venv .venv
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
```

3. Install Django and dependencies:
```bash
pip install django
pip install -r requirements.txt
```

4. Create a new Django project:
```bash
django-admin startproject cabinet
```

5. Create your Django application:
```bash
cd cabinet
python manage.py startapp medecin
```

## Database Setup

1. Create new migrations:
```bash
python manage.py makemigrations medecin
```

2. Apply migrations:
```bash
python manage.py migrate
```

3. Create admin superuser:
```bash
python manage.py createsuperuser
```

## Running the Application

Start the Django development server:
```bash
python manage.py runserver
```

## Access Points

Local Development:

- Django admin interface: http://127.0.0.1:8000/admin
- Main application: http://127.0.0.1:8000

Live Demo:

- Demo site: https://django33.pythonanywhere.com
- Demo admin interface: https://django33.pythonanywhere.com/admin

## Authentication

This application uses Django's built-in authentication system which provides:

- User registration
- Login/logout functionality
- Password management
- User permissions
- Group-based access control

## Security Notes
    
- All routes require authentication except the login page
- Passwords are securely hashed using Django's authentication system
- Session management is handled by Django's secure session framework

## Development

To contribute to this project:

1. Fork the repository 
2. Create a virtual environment 
3. Install dependencies 
4. Create a new branch for your feature 
5. Submit a pull request

