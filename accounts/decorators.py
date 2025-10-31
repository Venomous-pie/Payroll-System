from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import render


def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:

                return view_func(request, *args, **kwargs)
            

            if request.user.is_superuser or request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            

            return render(request, 'accounts/permission_denied.html', {
                'required_role': group_name,
                'user_roles': [group.name for group in request.user.groups.all()]
            }, status=403)
        
        return _wrapped_view
    return decorator
