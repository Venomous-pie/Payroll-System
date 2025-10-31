from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from accounts.utils import get_role_based_redirect_url

class Command(BaseCommand):
    help = 'Debug specific user redirection issue'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to debug')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(f'User "{username}" does not exist.')
            return
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(f'DEBUGGING USER REDIRECTION: {username}')
        self.stdout.write('='*60)
        

        groups = list(user.groups.all())
        group_names = [g.name for g in groups]
        
        self.stdout.write(f'Username: {user.username}')
        self.stdout.write(f'Email: {user.email}')
        self.stdout.write(f'First Name: {user.first_name}')
        self.stdout.write(f'Last Name: {user.last_name}')
        self.stdout.write(f'Is Superuser: {user.is_superuser}')
        self.stdout.write(f'Is Staff: {user.is_staff}')
        self.stdout.write(f'Is Active: {user.is_active}')
        self.stdout.write(f'Groups: {group_names}')
        

        self.stdout.write('\n--- REDIRECTION LOGIC DEBUG ---')
        

        if user.is_superuser:
            self.stdout.write('Step 1: User IS superuser -> Should redirect to /django-admin/')
            redirect_url = '/django-admin/'
        else:
            self.stdout.write('Step 1: User is NOT superuser -> Continue to group check')
            

            if user.groups.filter(name='Admin').exists():
                self.stdout.write('Step 2: User HAS Admin group -> Should redirect to /admin/')
                redirect_url = '/admin/'
            else:
                self.stdout.write('Step 2: User does NOT have Admin group -> Continue')
                

                if user.groups.filter(name='Staff').exists():
                    self.stdout.write('Step 3: User HAS Staff group -> Should redirect to /staff/')
                    redirect_url = '/staff/'
                else:
                    self.stdout.write('Step 3: User does NOT have Staff group -> Continue')
                    

                    if user.groups.filter(name='Employee').exists():
                        self.stdout.write('Step 4: User HAS Employee group -> Should redirect to /employee/')
                        redirect_url = '/employee/'
                    else:
                        self.stdout.write('Step 4: User does NOT have Employee group -> Use fallback')
                        redirect_url = '/employee/'
        

        actual_redirect = get_role_based_redirect_url(user)
        
        self.stdout.write('\n--- RESULTS ---')
        self.stdout.write(f'Expected redirect: {redirect_url}')
        self.stdout.write(f'Actual redirect: {actual_redirect}')
        
        if redirect_url == actual_redirect:
            self.stdout.write('STATUS: LOGIC IS CORRECT')
        else:
            self.stdout.write('STATUS: LOGIC ERROR DETECTED!')
        

        self.stdout.write('\n--- GROUP EXISTENCE CHECK ---')
        try:
            staff_group = Group.objects.get(name='Staff')
            self.stdout.write(f'Staff group exists: ID={staff_group.id}')
        except Group.DoesNotExist:
            self.stdout.write('ERROR: Staff group does NOT exist!')
        
        try:
            employee_group = Group.objects.get(name='Employee')
            self.stdout.write(f'Employee group exists: ID={employee_group.id}')
        except Group.DoesNotExist:
            self.stdout.write('ERROR: Employee group does NOT exist!')
        
        try:
            admin_group = Group.objects.get(name='Admin')
            self.stdout.write(f'Admin group exists: ID={admin_group.id}')
        except Group.DoesNotExist:
            self.stdout.write('ERROR: Admin group does NOT exist!')
        

        self.stdout.write('\n--- SUGGESTED FIX ---')
        if not user.groups.filter(name='Staff').exists():
            self.stdout.write('PROBLEM: User is not in Staff group!')
            self.stdout.write('SOLUTION: Add user to Staff group with:')
            self.stdout.write(f'  py manage.py shell')
            self.stdout.write(f'  from django.contrib.auth.models import User, Group')
            self.stdout.write(f'  user = User.objects.get(username="{username}")')
            self.stdout.write(f'  staff_group = Group.objects.get(name="Staff")')
            self.stdout.write(f'  user.groups.add(staff_group)')
        else:
            self.stdout.write('User is correctly in Staff group.')
            self.stdout.write('Check if there are conflicting middleware or URL issues.')
        
        self.stdout.write('\n' + '='*60)
