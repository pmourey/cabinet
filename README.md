
# Create new virtual environment
python3 -m venv .venv

# Activate the new environment
source .venv/bin/activate

# Install Django in the new environment:
pip install django

# Install dependencies
pip install -r requirements.txt

# Create new migration
python manage.py makemigrations

# Apply first migration
python manage.py migrate

# Create default user for authentication
python manage.py createsuperuser

# Run Django server
python manage.py runserver

# Connect to Django webapp or admin interface:
    Access the Django admin interface at http://127.0.0.1:8000/admin
    Access the Django web app at http://127.0.0.1:8000
