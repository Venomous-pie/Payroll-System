# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview
Django-based Payroll Management System (PMS) with role-based access control. Handles employee records, attendance tracking, payroll processing, and bank file generation for Philippine government contributions (SSS, PhilHealth, Pag-IBIG).

## Common Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Setup roles (creates Employee, Staff, Admin groups)
python manage.py setup_roles

# Create superuser
python manage.py createsuperuser
```

### Development
```bash
# Run development server
python manage.py runserver

# Run specific test
python manage.py test <app_name>.<test_class>.<test_method>

# Run all tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Access Django shell
python manage.py shell
```

## Architecture

### Role-Based Access Control
The system uses Django groups for hierarchical access:
- **Superuser**: Full access, redirects to `/django-admin/`
- **Admin group**: Management access, redirects to `/admin/`
- **Staff group**: HR/Payroll operations, redirects to `/staff/`
- **Employee group**: Self-service portal, redirects to `/employee/`

Role enforcement happens in two layers:
1. `RoleBasedAccessMiddleware` - Blocks unauthorized path access and redirects users
2. `@group_required` decorator - View-level protection with custom 403 pages

### App Structure

**accounts/**
- Custom authentication with `RoleBasedLoginView`
- `UserProfile` extends Django User with employee metadata
- `AuditLog` tracks all requests via `AuditLogMiddleware`
- `utils.py` contains role detection helpers (`get_role_based_redirect_url`, `user_has_role`)

**employees/**
- `Employee` model with `salary_grade` FK for pay computation
- `SalaryGrade` model defines code, step, and base_pay
- Each employee linked to Django User via OneToOne

**attendance/**
- `AttendanceLog` - daily time in/out (unique per employee+date)
- `LeaveRequest` - approval workflow (PENDING/APPROVED/REJECTED)

**payroll/**
- `PayrollRun` - period-based payroll batch
- `Payslip` - computed pay with government contributions
- `Loan` - tracks employee loans with monthly deductions
- `OtherDeduction` - misc deductions (uniform, tools)
- `utils.py` - payroll computation logic:
  - `compute_contributions()` - SSS, PhilHealth, Pag-IBIG, tax
  - `compute_employee_deductions()` - loans and other deductions
  - `compute_full_payroll()` - complete payslip calculation
  - `generate_bank_file()` - CSV export for salary deposits

**dashboards/**
- Three separate URL configs: `admin_urls.py`, `staff_urls.py`, `employee_urls.py`
- Single `views.py` with role-specific dashboard views
- Staff dashboard includes staff app URLs via `include('staff.urls')`

**reports/**
- Reporting functionality (structure TBD)

**staff/**
- HR/Staff-specific features nested under `/staff/` path

### URL Routing
- Root `/` → `home_view` redirects by role
- `/accounts/` → auth (login/logout)
- `/employee/` → employee dashboard
- `/staff/` → staff dashboard + staff app features
- `/admin/` → admin dashboard
- `/django-admin/` → Django admin panel
- `/employees/`, `/attendance/`, `/payroll/`, `/reports/` → respective app features

### Settings Notes
- Database: SQLite (`db.sqlite3`)
- Timezone: `Asia/Manila`
- Environment vars: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
- Custom middleware order matters: `AuditLogMiddleware` → `RoleBasedAccessMiddleware`
- Templates have `user_roles` context processor

### Payroll Computation Flow
1. Get employee's base pay from `salary_grade.base_pay`
2. Add overtime pay
3. Compute government contributions (SSS, PhilHealth, Pag-IBIG, tax)
4. Compute employee deductions (active loans, other deductions)
5. Calculate net pay = gross - all deductions
6. Create `Payslip` record
7. Generate bank file CSV for salary transfer
