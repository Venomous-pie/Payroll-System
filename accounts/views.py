from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserProfileForm
from .models import UserProfile
from .utils import redirect_user_by_role, get_role_based_redirect_url

class RoleBasedLoginView(LoginView):
    """Custom login view that redirects users based on their role"""
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return get_role_based_redirect_url(self.request.user)
    
    def form_valid(self, form):
        """Add success message on login"""
        response = super().form_valid(form)
        user = self.request.user
        

        if user.is_superuser:
            role = "Superuser"
        elif user.groups.filter(name='Admin').exists():
            role = "Administrator"
        elif user.groups.filter(name='Staff').exists():
            role = "Staff/HR"
        else:
            role = "Employee"
        
        messages.success(
            self.request, 
            f'Welcome back, {user.get_full_name() or user.username}! '
            f'You are logged in as {role}.'
        )
        return response

class CustomLogoutView(LogoutView):
    """Custom logout view with success message"""
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile_update(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_update')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form})

def home_view(request):
    """
    Role-aware home view that redirects users to their appropriate dashboard.
    Shows landing page for non-authenticated users.
    """
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)
    else:
        return render(request, 'accounts/landing.html')
