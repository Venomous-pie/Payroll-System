from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from accounts.utils import get_role_based_redirect_url

class Command(BaseCommand):
    help = 'Verify all role-based redirections are working correctly'

    def handle(self, *args, **options):

        staff_group, _ = Group.objects.get_or_create(name='Staff')
        employee_group, _ = Group.objects.get_or_create(name='Employee')
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('COMPREHENSIVE ROLE REDIRECTION TEST')
        self.stdout.write('='*60)
        

        staff_user, _ = User.objects.get_or_create(
            username='test_staff_redirect',
            defaults={'email': 'staff@test.com', 'first_name': 'Staff', 'last_name': 'User'}
        )
        staff_user.groups.clear()
        staff_user.groups.add(staff_group)
        staff_user.is_superuser = False
        staff_user.save()
        
        staff_redirect = get_role_based_redirect_url(staff_user)
        self.test_redirect(staff_user, staff_redirect, '/staff/', 'Staff User')
        

        emp_user, _ = User.objects.get_or_create(
            username='test_emp_redirect',
            defaults={'email': 'emp@test.com', 'first_name': 'Employee', 'last_name': 'User'}
        )
        emp_user.groups.clear()
        emp_user.groups.add(employee_group)
        emp_user.is_superuser = False
        emp_user.save()
        
        emp_redirect = get_role_based_redirect_url(emp_user)
        self.test_redirect(emp_user, emp_redirect, '/employee/', 'Employee User')
        

        admin_user, _ = User.objects.get_or_create(
            username='test_admin_redirect',
            defaults={'email': 'admin@test.com', 'first_name': 'Admin', 'last_name': 'User'}
        )
        admin_user.groups.clear()
        admin_user.groups.add(admin_group)
        admin_user.is_superuser = False
        admin_user.save()
        
        admin_redirect = get_role_based_redirect_url(admin_user)
        self.test_redirect(admin_user, admin_redirect, '/admin/', 'Admin User')
        

        super_user, _ = User.objects.get_or_create(
            username='test_super_redirect',
            defaults={'email': 'super@test.com', 'first_name': 'Super', 'last_name': 'User'}
        )
        super_user.groups.clear()
        super_user.is_superuser = True
        super_user.save()
        
        super_redirect = get_role_based_redirect_url(super_user)
        self.test_redirect(super_user, super_redirect, '/django-admin/', 'Superuser')
        

        no_group_user, _ = User.objects.get_or_create(
            username='test_nogroup_redirect',
            defaults={'email': 'nogroup@test.com', 'first_name': 'NoGroup', 'last_name': 'User'}
        )
        no_group_user.groups.clear()
        no_group_user.is_superuser = False
        no_group_user.save()
        
        nogroup_redirect = get_role_based_redirect_url(no_group_user)
        self.test_redirect(no_group_user, nogroup_redirect, '/employee/', 'User with No Groups (Fallback)')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('ROLE REDIRECTION TEST COMPLETE')
        self.stdout.write('='*60)
        
        self.stdout.write('\nTest Users Created:')
        self.stdout.write('• test_staff_redirect / testpass123 → /staff/')
        self.stdout.write('• test_emp_redirect / testpass123 → /employee/')
        self.stdout.write('• test_admin_redirect / testpass123 → /admin/')
        self.stdout.write('• test_super_redirect / testpass123 → /django-admin/')
        self.stdout.write('• test_nogroup_redirect / testpass123 → /employee/ (fallback)')
        
    def test_redirect(self, user, actual_url, expected_url, user_type):
        groups = [g.name for g in user.groups.all()]
        status = '[PASS]' if actual_url == expected_url else '[FAIL]'
        
        self.stdout.write(f'\n{status} {user_type}:')
        self.stdout.write(f'  Username: {user.username}')
        self.stdout.write(f'  Groups: {groups}')
        self.stdout.write(f'  Is Superuser: {user.is_superuser}')
        self.stdout.write(f'  Actual URL: {actual_url}')
        self.stdout.write(f'  Expected URL: {expected_url}')
        
        if actual_url != expected_url:
            self.stdout.write(f'  ERROR: Redirection not working correctly!')
        else:
            self.stdout.write(f'  SUCCESS: Redirection working correctly!')
