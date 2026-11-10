import os
from django.apps import AppConfig
from django.contrib.auth import get_user_model

class RecruitmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recruitment'

    def ready(self):
        # Prevent running twice during autoreload
        if os.environ.get('RUN_MAIN'):
            return

        # Fetch credentials securely from Render Environment Variables
        username = os.environ.get('CREATE_SUPERUSER_USERNAME')
        password = os.environ.get('CREATE_SUPERUSER_PASSWORD')
        email = os.environ.get('CREATE_SUPERUSER_EMAIL', 'admin@example.com')

        if username and password:
            try:
                User = get_user_model()
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(username=username, email=email, password=password)
                    print(f"Superuser '{username}' created successfully!")
            except Exception as e:
                print(f"Superuser creation skipped: {e}")
