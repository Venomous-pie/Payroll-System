from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from accounts.utils import get_role_based_redirect_url

class Command(BaseCommand):
    help = 'Test Staff user redirection specifically'

    def handle(self, *args, **options):

        staff_group, _ = Group.objects.get_or_create(name='Staff')
        employee_group, _ = Group.objects.get_or_create(name='Employee')
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        

        staff_user, created = User.objects.get_or_create(
            username='test_staff_user',
            defaults={
                'email': 'staff@example.com',
                'first_name': 'Test',
                'last_name': 'Staff',
            }
        )
        
        if created:
            staff_user.set_password('testpass123')
            staff_user.save()
            self.stdout.write('Created test staff user')
        

        staff_user.groups.clear()
        

        staff_user.groups.add(staff_group)
        

        redirect_url = get_role_based_redirect_url(staff_user)
        expected_url = '/staff/'
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('TESTING STAFF USER REDIRECTION')
        self.stdout.write('='*50)
        
        self.stdout.write(f'User: {staff_user.username}')
        self.stdout.write(f'Groups: {[g.name for g in staff_user.groups.all()]}')
        self.stdout.write(f'Is Superuser: {staff_user.is_superuser}')
        self.stdout.write(f'Redirect URL: {redirect_url}')
        self.stdout.write(f'Expected URL: {expected_url}')
        
        if redirect_url == expected_url:
            self.stdout.write('[PASS] Staff user redirection working correctly!')
        else:
            self.stdout.write('[FAIL] Staff user redirection not working!')
        
        self.stdout.write('\nTest login credentials:')
        self.stdout.write('Username: test_staff_user')
        self.stdout.write('Password: testpass123')
        self.stdout.write('Expected redirect: /staff/')
        

        from accounts.utils import user_has_role
        self.stdout.write('\nHierarchical Access Test:')
        self.stdout.write(f'Has Staff role: {user_has_role(staff_user, "Staff")}')
        self.stdout.write(f'Has Employee access: {user_has_role(staff_user, "Employee")}')
        self.stdout.write(f'Has Admin role: {user_has_role(staff_user, "Admin")}')
        
        self.stdout.write('\n' + '='*50)
