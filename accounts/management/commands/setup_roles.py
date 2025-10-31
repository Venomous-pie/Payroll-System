from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create default user groups and setup role-based system'

    def handle(self, *args, **options):

        groups = ['Employee', 'Staff', 'Admin']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(f'Group already exists: {group_name}')
        
        self.stdout.write(
            self.style.SUCCESS('\nRole setup complete!')
        )
        self.stdout.write('\nTo assign roles to users:')
        self.stdout.write('1. Go to Django admin (/django-admin/)')
        self.stdout.write('2. Navigate to Users')
        self.stdout.write('3. Edit a user and assign them to appropriate groups')
        self.stdout.write('\nRole hierarchy:')
        self.stdout.write('- Superuser: Redirects to /django-admin/')
        self.stdout.write('- Admin group: Redirects to /admin/')
        self.stdout.write('- Staff group: Redirects to /staff/')
        self.stdout.write('- Employee group: Redirects to /employee/')
        self.stdout.write('- Default (no group): Redirects to /employee/')
