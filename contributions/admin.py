from django.contrib import admin
from .models import SSSContributionTable, PhilHealthContributionTable, PagibigContributionTable, TaxTable

@admin.register(SSSContributionTable)
class SSSContributionTableAdmin(admin.ModelAdmin):
    list_display = ['min_salary', 'max_salary', 'employee_share', 'employer_share', 'ec_share', 'total', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']
    search_fields = ['min_salary', 'max_salary']

@admin.register(PhilHealthContributionTable)
class PhilHealthContributionTableAdmin(admin.ModelAdmin):
    list_display = ['premium_rate', 'max_contribution', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']

@admin.register(PagibigContributionTable)
class PagibigContributionTableAdmin(admin.ModelAdmin):
    list_display = ['employee_rate', 'employer_rate', 'max_employee_contribution', 'max_employer_contribution', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']

@admin.register(TaxTable)
class TaxTableAdmin(admin.ModelAdmin):
    list_display = ['min_compensation', 'max_compensation', 'base_tax', 'tax_rate', 'effective_date', 'is_active']
    list_filter = ['is_active', 'effective_date']
    search_fields = ['min_compensation']
