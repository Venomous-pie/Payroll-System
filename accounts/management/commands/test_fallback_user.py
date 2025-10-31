from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.utils import get_role_based_redirect_url

class Command(BaseCommand):
    help = 'Test fallback user redirection (user without groups)'

    def handle(self, *args, **options):

        user, created = User.objects.get_or_create(
            username='no_group_user',
            defaults={
                'email': 'nogroup@example.com',
                'first_name': 'No Group',
                'last_name': 'User',
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write('Created user without groups: no_group_user')
        

        redirect_url = get_role_based_redirect_url(user)
        expected_url = '/employee/'
        
        status = "[PASS]" if redirect_url == expected_url else "[FAIL]"
        self.stdout.write(f'{status} no_group_user: {redirect_url} (expected: {expected_url})')
        
        self.stdout.write('\nFallback test complete!')
        self.stdout.write('Users without groups should redirect to /employee/ dashboard')
        self.stdout.write('Login with: no_group_user / testpass123')
