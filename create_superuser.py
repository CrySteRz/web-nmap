import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_pass = os.environ.get('ADMIN_PASS')
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', admin_email, admin_pass)
        print("Superuser created.")
    else:
        print("Superuser already exists.")

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scandere.settings')
    django.setup()
    create_superuser()
