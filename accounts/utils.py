from django.shortcuts import redirect
from django.urls import reverse

def get_role_based_redirect_url(user):
    """
    Returns the appropriate URL based on user's role/group membership.
    
    Priority order:
    1. Superuser -> Django admin
    2. Admin group -> Admin dashboard
    3. Staff group -> Staff dashboard
    4. Employee group -> Employee dashboard
    5. Default -> Employee dashboard
    """

    if user.is_superuser:
        return '/django-admin/'
    

    if user.groups.filter(name='Admin').exists():
        return '/admin/'
    

    if user.groups.filter(name='Staff').exists():
        return '/staff/'
    

    if user.groups.filter(name='Employee').exists():
        return '/employee/'
    

    return '/employee/'

def redirect_user_by_role(user):
    """
    Returns a redirect response based on user's role.
    """
    return redirect(get_role_based_redirect_url(user))

def user_has_role(user, role_name):
    """
    Check if user has a specific role (group membership).
    Superusers are considered to have all roles.
    Staff and Admin users have access to Employee features (hierarchical access).
    """
    if user.is_superuser:
        return True
    

    if user.groups.filter(name=role_name).exists():
        return True
    

    if role_name == 'Employee':

        return (user.groups.filter(name='Staff').exists() or 
                user.groups.filter(name='Admin').exists())
    elif role_name == 'Staff':

        return user.groups.filter(name='Admin').exists()
    
    return False
