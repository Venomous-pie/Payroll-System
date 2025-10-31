from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('django-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employee/', include('dashboards.employee_urls')),
    path('admin/', include('dashboards.admin_urls')),

    path('staff/', include('dashboards.staff_urls')),  # This handles /staff/ -> staff dashboard + all staff features
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('payroll/', include('payroll.urls')),
    path('reports/', include('reports.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
