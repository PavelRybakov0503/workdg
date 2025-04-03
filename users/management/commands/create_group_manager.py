from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create permissions and groups"

    def handle(self, *args, **options):
        manager_group = Group.objects.create(name="Manager")

        view_user_list = Permission.objects.get(codename="can_view_user_list")
        blocking_user = Permission.objects.get(codename="can_blocking_user")
        view_mailings = Permission.objects.get(codename="can_view_mailing")
        disabling_mailing = Permission.objects.get(codename="can_disabling_mailing")

        manager_group.permissions.add(view_user_list, blocking_user, view_mailings, disabling_mailing)
        manager_group.save()
        self.stdout.write(self.style.SUCCESS("Permissions and groups created successfully"))
