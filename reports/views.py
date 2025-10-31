from django.contrib.auth.decorators import login_required
from accounts.decorators import group_required
from django.http import HttpResponse
from django.shortcuts import render
import csv

@login_required
@group_required('Staff')
def index(request):
    return render(request, 'reports/index.html')

@login_required
@group_required('Staff')
def bir_summary(request):
    return render(request, 'reports/bir_summary.html')

@login_required
@group_required('Staff')
def gsis_summary(request):
    return render(request, 'reports/gsis_summary.html')

@login_required
@group_required('Staff')
def export_csv(request, kind: str):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{kind}_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Field A', 'Field B', 'Field C'])
    writer.writerow(['Sample 1', 'Sample 2', 'Sample 3'])
    return response
