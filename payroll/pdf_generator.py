"""
PDF Payslip Generator using ReportLab
"""
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from django.conf import settings
from decimal import Decimal


class PayslipPDFGenerator:
    """Generate professional payslip PDFs"""
    
    def __init__(self, payslip):
        self.payslip = payslip
        self.employee = payslip.employee
        self.payroll_run = payslip.payroll_run
        
    def generate(self):
        """Generate PDF and return BytesIO buffer"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
        )
        
        # Company Header
        story.append(Paragraph("PAYROLL MANAGEMENT SYSTEM", title_style))
        story.append(Paragraph("PAYSLIP", styles['Heading2']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Employee Information
        emp_data = [
            ['Employee Name:', f"{self.employee.first_name} {self.employee.last_name}"],
            ['Employee No:', self.employee.employee_no],
            ['Department:', self.employee.department],
            ['Position:', self.employee.position],
            ['Period:', f"{self.payroll_run.period_start} to {self.payroll_run.period_end}"],
        ]
        
        emp_table = Table(emp_data, colWidths=[2*inch, 4*inch])
        emp_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(emp_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Earnings Section
        story.append(Paragraph("EARNINGS", heading_style))
        
        earnings_data = [
            ['Description', 'Amount'],
            ['Basic Pay', self._format_currency(self.payslip.gross_pay)],
        ]
        
        if self.payslip.overtime_pay > 0:
            earnings_data.append(['Overtime Pay', self._format_currency(self.payslip.overtime_pay)])
        if self.payslip.holiday_pay > 0:
            earnings_data.append(['Holiday Pay', self._format_currency(self.payslip.holiday_pay)])
        if self.payslip.night_differential > 0:
            earnings_data.append(['Night Differential', self._format_currency(self.payslip.night_differential)])
        if self.payslip.allowances > 0:
            earnings_data.append(['Allowances', self._format_currency(self.payslip.allowances)])
        
        earnings_data.append(['TOTAL EARNINGS', self._format_currency(self.payslip.total_earnings)])
        
        earnings_table = Table(earnings_data, colWidths=[4*inch, 2*inch])
        earnings_table.setStyle(self._get_table_style())
        story.append(earnings_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Deductions Section
        story.append(Paragraph("DEDUCTIONS", heading_style))
        
        deductions_data = [
            ['Description', 'Amount'],
            ['SSS Contribution', self._format_currency(self.payslip.sss)],
            ['PhilHealth', self._format_currency(self.payslip.philhealth)],
            ['Pag-IBIG', self._format_currency(self.payslip.pagibig)],
            ['Withholding Tax', self._format_currency(self.payslip.tax)],
        ]
        
        if self.payslip.loan_deductions > 0:
            deductions_data.append(['Loan Deductions', self._format_currency(self.payslip.loan_deductions)])
        if self.payslip.other_deductions > 0:
            deductions_data.append(['Other Deductions', self._format_currency(self.payslip.other_deductions)])
        
        deductions_data.append(['TOTAL DEDUCTIONS', self._format_currency(self.payslip.total_deductions)])
        
        deductions_table = Table(deductions_data, colWidths=[4*inch, 2*inch])
        deductions_table.setStyle(self._get_table_style())
        story.append(deductions_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Net Pay Section
        net_pay_data = [
            ['NET PAY', self._format_currency(self.payslip.net_pay)],
        ]
        
        net_pay_table = Table(net_pay_data, colWidths=[4*inch, 2*inch])
        net_pay_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#16a34a')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dcfce7')),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#16a34a')),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(net_pay_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Attendance Details
        if self.payslip.days_worked > 0:
            story.append(Paragraph("ATTENDANCE", heading_style))
            attendance_data = [
                ['Days Worked', str(self.payslip.days_worked)],
                ['Overtime Hours', str(self.payslip.overtime_hours)],
                ['Absences', str(self.payslip.absences)],
            ]
            
            attendance_table = Table(attendance_data, colWidths=[4*inch, 2*inch])
            attendance_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ]))
            story.append(attendance_table)
            story.append(Spacer(1, 0.3 * inch))
        
        # Footer
        footer_text = "This is a computer-generated payslip. No signature required."
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _format_currency(self, amount):
        """Format decimal as Philippine Peso currency"""
        return f"₱{amount:,.2f}"
    
    def _get_table_style(self):
        """Common table style"""
        return TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])


def generate_payslip_pdf(payslip):
    """Generate PDF for a payslip and return buffer"""
    generator = PayslipPDFGenerator(payslip)
    return generator.generate()
