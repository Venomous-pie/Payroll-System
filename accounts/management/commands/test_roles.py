from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from accounts.utils import get_role_based_redirect_url, user_has_role

User = get_user_model()

class Command(BaseCommand):
    help = 'Test role-based redirection system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-test-users',
            action='store_true',
            help='Create test users for each role',
        )

    def handle(self, *args, **options):
        if options['create_test_users']:
            self.create_test_users()
        
        self.test_role_redirections()

    def create_test_users(self):
        """Create test users for each role"""
        self.stdout.write('Creating test users...')
        

        groups = ['Employee', 'Staff', 'Admin']
        for group_name in groups:
            Group.objects.get_or_create(name=group_name)
        

        test_users = [
            ('employee_user', 'Employee'),
            ('staff_user', 'Staff'),
            ('admin_user', 'Admin'),
        ]
        
        for username, group_name in test_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': username.replace('_', ' ').title(),
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            

            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            self.stdout.write(f'Added {username} to {group_name} group')
        

        superuser, created = User.objects.get_or_create(
            username='superuser',
            defaults={
                'email': 'superuser@example.com',
                'is_superuser': True,
                'is_staff': True,
            }
        )
        if created:
            superuser.set_password('superpass123')
            superuser.save()
            self.stdout.write('Created superuser')

    def test_role_redirections(self):
        """Test role-based redirection logic"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('TESTING ROLE-BASED REDIRECTIONS')
        self.stdout.write('='*50)
        

        test_cases = [
            ('employee_user', '/employee/'),
            ('staff_user', '/staff/'),
            ('admin_user', '/admin/'),
            ('superuser', '/django-admin/'),
        ]
        
        for username, expected_url in test_cases:
            try:
                user = User.objects.get(username=username)
                actual_url = get_role_based_redirect_url(user)
                
                status = "[PASS]" if actual_url == expected_url else "[FAIL]"
                self.stdout.write(f'{status} {username}: {actual_url} (expected: {expected_url})')
                

                if username != 'superuser':
                    group_name = username.split('_')[0].title()
                    has_role = user_has_role(user, group_name)
                    role_status = "[OK]" if has_role else "[NO]"
                    self.stdout.write(f'    {role_status} Has {group_name} role: {has_role}')
                
            except User.DoesNotExist:
                self.stdout.write(f'[SKIP] {username}: User does not exist')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('TEST COMPLETE')
        self.stdout.write('='*50)
        

        self.stdout.write('\nTo test the login system:')
        self.stdout.write('1. Run: python manage.py runserver')
        self.stdout.write('2. Go to: http://localhost:8000/accounts/login/')
        self.stdout.write('3. Try logging in with:')
        self.stdout.write('   - employee_user / testpass123 -> Should redirect to /employee/')
        self.stdout.write('   - staff_user / testpass123 -> Should redirect to /staff/')
        self.stdout.write('   - admin_user / testpass123 -> Should redirect to /admin/')
        self.stdout.write('   - superuser / superpass123 -> Should redirect to /django-admin/')
        self.stdout.write('\n4. Try accessing unauthorized URLs to test middleware protection')
