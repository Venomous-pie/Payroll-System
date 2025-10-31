from .utils import user_has_role

def user_roles(request):
    """
    Context processor to make user role information available in templates.
    """
    if request.user.is_authenticated:
        return {
            'user_is_admin': user_has_role(request.user, 'Admin'),
            'user_is_staff': user_has_role(request.user, 'Staff'),
            'user_is_employee': user_has_role(request.user, 'Employee'),
            'user_is_superuser': request.user.is_superuser,
        }
    return {
        'user_is_admin': False,
        'user_is_staff': False,
        'user_is_employee': False,
        'user_is_superuser': False,
    }
