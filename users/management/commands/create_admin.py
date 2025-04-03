from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser"

    def handle(self, *args, **options):
        User = get_user_model()

        user = User.objects.create(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
        )
        user.set_password("admin")
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Superuser created: {user.email}"))
