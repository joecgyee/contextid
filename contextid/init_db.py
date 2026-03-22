import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contextid.settings')
django.setup()

from django.contrib.auth.models import User

def seed():
    # 1. Create Superuser if not exists
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'superuser')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'superuser@email.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if password and not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser {username} created.")

if __name__ == '__main__':
    seed()