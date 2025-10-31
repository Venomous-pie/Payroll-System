from .models import AuditLog
from django.shortcuts import redirect
from django.urls import resolve
from .utils import get_role_based_redirect_url, user_has_role

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            AuditLog.objects.create(
                user=request.user if getattr(request, 'user', None) and request.user.is_authenticated else None,
                path=request.path,
                method=request.method,
                ip=request.META.get('REMOTE_ADDR', ''),
                status_code=response.status_code,
            )
        except Exception:

            pass
        return response

class RoleBasedAccessMiddleware:
    """
    Middleware to enforce role-based access control.
    Redirects users to appropriate dashboards if they try to access unauthorized areas.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        skip_paths = [
            '/accounts/login/',
            '/accounts/logout/',
            '/django-admin/',
            '/static/',
            '/media/',
        ]
        

        if any(request.path.startswith(path) for path in skip_paths):
            return self.get_response(request)
        

        if not request.user.is_authenticated:
            return self.get_response(request)
        

        role_paths = {
            '/admin/': ['Admin'],
            '/staff/': ['Staff', 'Admin'],

        }
        

        for path_prefix, allowed_roles in role_paths.items():
            if request.path.startswith(path_prefix):

                if request.user.is_superuser:
                    break
                

                has_access = any(user_has_role(request.user, role) for role in allowed_roles)
                
                if not has_access:

                    return redirect(get_role_based_redirect_url(request.user))
                break
        
        return self.get_response(request)
