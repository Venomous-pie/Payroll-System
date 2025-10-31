@echo off
REM ============================================================================
REM Payroll System - Complete Demo Setup Script
REM ============================================================================
REM This script will:
REM 1. Delete existing database
REM 2. Run migrations
REM 3. Seed the system with 14 months of data
REM 4. Start the development server
REM ============================================================================

echo.
echo ============================================================================
echo          PAYROLL SYSTEM - DEMO SETUP
echo ============================================================================
echo.
echo This will set up a fresh demo environment with:
echo   - 15 Employees
echo   - 14 Months of historical data
echo   - Attendance records, payroll runs, loans, and more
echo.
echo WARNING: This will DELETE the existing database!
echo.
pause

echo.
echo [1/5] Deleting existing database...
if exist db.sqlite3 (
    del db.sqlite3
    echo    Database deleted.
) else (
    echo    No existing database found.
)

echo.
echo [2/5] Running migrations...
venv\Scripts\python.exe manage.py migrate

echo.
echo [3/5] Seeding system with demo data (this may take 30-60 seconds)...
venv\Scripts\python.exe manage.py seed_complete_system --months 14

echo.
echo ============================================================================
echo          SETUP COMPLETE!
echo ============================================================================
echo.
echo Login Credentials:
echo.
echo   ADMIN (Full Access):
echo     URL: http://127.0.0.1:8000/django-admin/
echo     Username: admin
echo     Password: admin123
echo.
echo   HR STAFF (Payroll Processing):
echo     URL: http://127.0.0.1:8000/accounts/login/
echo     Username: hr_staff
echo     Password: staff123
echo.
echo   EMPLOYEES (Self-Service):
echo     URL: http://127.0.0.1:8000/accounts/login/
echo     Username: employee1, employee2, ..., employee15
echo     Password: password123
echo.
echo ============================================================================
echo.
echo [4/5] Starting development server...
echo.
echo Press Ctrl+C to stop the server when done.
echo.
pause

echo.
echo [5/5] Launching server...
start http://127.0.0.1:8000
venv\Scripts\python.exe manage.py runserver

echo.
echo Server stopped.
pause
