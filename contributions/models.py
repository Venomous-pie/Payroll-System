from django.db import models
from decimal import Decimal

class SSSContributionTable(models.Model):
    """SSS contribution table based on salary range"""
    min_salary = models.DecimalField(max_digits=12, decimal_places=2)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2)
    employee_share = models.DecimalField(max_digits=12, decimal_places=2)
    employer_share = models.DecimalField(max_digits=12, decimal_places=2)
    ec_share = models.DecimalField(max_digits=12, decimal_places=2, default=10.00)  # Employer Compensation
    total = models.DecimalField(max_digits=12, decimal_places=2)
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['min_salary']
        
    def __str__(self):
        return f"SSS: ₱{self.min_salary} - ₱{self.max_salary}"
    
    @classmethod
    def get_contribution(cls, salary):
        """Get SSS contribution for given salary"""
        try:
            row = cls.objects.filter(
                is_active=True,
                min_salary__lte=salary,
                max_salary__gte=salary
            ).first()
            
            if not row:
                # If salary is above max, use the highest bracket
                row = cls.objects.filter(is_active=True).order_by('-max_salary').first()
            
            return {
                'employee': row.employee_share if row else Decimal('0.00'),
                'employer': row.employer_share if row else Decimal('0.00'),
                'ec': row.ec_share if row else Decimal('0.00'),
                'total': row.total if row else Decimal('0.00')
            }
        except:
            return {'employee': Decimal('0.00'), 'employer': Decimal('0.00'), 'ec': Decimal('0.00'), 'total': Decimal('0.00')}


class PhilHealthContributionTable(models.Model):
    """PhilHealth contribution table"""
    min_salary = models.DecimalField(max_digits=12, decimal_places=2)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    premium_rate = models.DecimalField(max_digits=5, decimal_places=4)  # e.g., 0.05 for 5%
    max_contribution = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['effective_date']
        
    def __str__(self):
        return f"PhilHealth: {self.premium_rate * 100}% (Effective: {self.effective_date})"
    
    @classmethod
    def get_contribution(cls, salary):
        """Get PhilHealth contribution for given salary"""
        try:
            table = cls.objects.filter(is_active=True).order_by('-effective_date').first()
            if not table:
                return {'employee': Decimal('0.00'), 'employer': Decimal('0.00'), 'total': Decimal('0.00')}
            
            # Calculate based on salary
            contribution = salary * table.premium_rate
            
            # Apply max cap if exists
            if table.max_contribution and contribution > table.max_contribution:
                contribution = table.max_contribution
            
            # Split 50-50 between employee and employer
            employee_share = contribution / 2
            employer_share = contribution / 2
            
            return {
                'employee': employee_share.quantize(Decimal('0.01')),
                'employer': employer_share.quantize(Decimal('0.01')),
                'total': contribution.quantize(Decimal('0.01'))
            }
        except:
            return {'employee': Decimal('0.00'), 'employer': Decimal('0.00'), 'total': Decimal('0.00')}


class PagibigContributionTable(models.Model):
    """Pag-IBIG contribution table"""
    min_salary = models.DecimalField(max_digits=12, decimal_places=2)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    employee_rate = models.DecimalField(max_digits=5, decimal_places=4)  # e.g., 0.02 for 2%
    employer_rate = models.DecimalField(max_digits=5, decimal_places=4)
    max_employee_contribution = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_employer_contribution = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['effective_date']
        
    def __str__(self):
        return f"Pag-IBIG: EE {self.employee_rate * 100}%, ER {self.employer_rate * 100}%"
    
    @classmethod
    def get_contribution(cls, salary):
        """Get Pag-IBIG contribution for given salary"""
        try:
            table = cls.objects.filter(is_active=True).order_by('-effective_date').first()
            if not table:
                return {'employee': Decimal('0.00'), 'employer': Decimal('0.00'), 'total': Decimal('0.00')}
            
            # Calculate employee share
            employee_share = salary * table.employee_rate
            if table.max_employee_contribution and employee_share > table.max_employee_contribution:
                employee_share = table.max_employee_contribution
            
            # Calculate employer share
            employer_share = salary * table.employer_rate
            if table.max_employer_contribution and employer_share > table.max_employer_contribution:
                employer_share = table.max_employer_contribution
            
            return {
                'employee': employee_share.quantize(Decimal('0.01')),
                'employer': employer_share.quantize(Decimal('0.01')),
                'total': (employee_share + employer_share).quantize(Decimal('0.01'))
            }
        except:
            return {'employee': Decimal('0.00'), 'employer': Decimal('0.00'), 'total': Decimal('0.00')}


class TaxTable(models.Model):
    """BIR Withholding Tax Table"""
    min_compensation = models.DecimalField(max_digits=12, decimal_places=2)
    max_compensation = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    base_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4)  # e.g., 0.20 for 20%
    effective_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['min_compensation']
        
    def __str__(self):
        return f"Tax: ₱{self.min_compensation}+ @ {self.tax_rate * 100}%"
    
    @classmethod
    def get_withholding_tax(cls, annual_taxable_income):
        """Calculate withholding tax based on annual taxable income"""
        try:
            if annual_taxable_income <= Decimal('250000'):
                return Decimal('0.00')
            
            tax_bracket = cls.objects.filter(
                is_active=True,
                min_compensation__lte=annual_taxable_income
            ).order_by('-min_compensation').first()
            
            if not tax_bracket:
                return Decimal('0.00')
            
            excess = annual_taxable_income - tax_bracket.min_compensation
            tax = tax_bracket.base_tax + (excess * tax_bracket.tax_rate)
            
            return tax.quantize(Decimal('0.01'))
        except:
            return Decimal('0.00')
