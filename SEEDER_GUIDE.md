# Employee Seeder Guide

## 🌱 What Was Created

A Django management command that automatically creates **10 sample employees** with realistic data.

---

## 🚀 How to Use

### **Run the Seeder:**

```bash
# Activate virtual environment first (if not already active)
venv\Scripts\activate

# Run the seeder
python manage.py seed_employees
```

---

## 👥 What Gets Created

### **10 Employees:**

| Employee # | Name | Username | Password |
|------------|------|----------|----------|
| EMP001 | Juan Dela Cruz | employee1 | password123 |
| EMP002 | Maria Santos | employee2 | password123 |
| EMP003 | Jose Reyes | employee3 | password123 |
| EMP004 | Ana Garcia | employee4 | password123 |
| EMP005 | Pedro Ramos | employee5 | password123 |
| EMP006 | Rosa Torres | employee6 | password123 |
| EMP007 | Carlos Flores | employee7 | password123 |
| EMP008 | Elena Mendoza | employee8 | password123 |
| EMP009 | Miguel Castro | employee9 | password123 |
| EMP010 | Sofia Bautista | employee10 | password123 |

### **Each Employee Has:**
- ✅ User account (for login)
- ✅ Employee record
- ✅ Random department (Accounting, HR, IT, Sales, Operations, Marketing)
- ✅ Random position (Staff, Senior Staff, Supervisor, Manager, Specialist)
- ✅ Random salary grade (SG1-SG5)
- ✅ Random hire date (1 month to 2 years ago)
- ✅ Random bank (BDO, BPI, Metrobank, UnionBank, Security Bank)
- ✅ Random bank account number
- ✅ Active status

### **5 Salary Grades (Auto-created if none exist):**

| Code | Base Pay |
|------|----------|
| SG1-Step1 | ₱15,000.00 |
| SG2-Step1 | ₱20,000.00 |
| SG3-Step1 | ₱25,000.00 |
| SG4-Step1 | ₱30,000.00 |
| SG5-Step1 | ₱40,000.00 |

---

## 🔐 Login Credentials

### **To Test as Employee:**
```
URL: http://127.0.0.1:8000/accounts/login/
Username: employee1 (or employee2, employee3, etc.)
Password: password123
```

### **To View All Employees (as Staff/Admin):**
```
URL: http://127.0.0.1:8000/employees/
```

---

## ✨ Features

### **Smart Seeding:**
- ✅ **Checks for duplicates** - Won't create if employee already exists
- ✅ **Auto-creates salary grades** - If none exist
- ✅ **Realistic data** - Random but sensible combinations
- ✅ **Safe to re-run** - Skips existing records

### **Sample Output:**
```
Starting employee seeding...
✓ Created: EMP001 - Dela Cruz, Juan (HR - Senior Staff)
✓ Created: EMP002 - Santos, Maria (Accounting - Specialist)
...
============================================================
✓ Successfully created 10 employees
============================================================
```

---

## 🔧 Customization

### **To Change Number of Employees:**

Edit `employees/management/commands/seed_employees.py`:

```python
# Change this line:
for i in range(1, 11):  # Creates 10 employees

# To:
for i in range(1, 21):  # Creates 20 employees
```

### **To Add More Names:**

```python
first_names = ['Juan', 'Maria', 'Jose', ...]  # Add more names
last_names = ['Dela Cruz', 'Santos', ...]     # Add more names
```

### **To Change Default Password:**

```python
user = User.objects.create_user(
    username=username,
    password='your_new_password',  # Change here
    ...
)
```

---

## 🗑️ Reset/Delete All Seeded Employees

### **Option 1: Django Shell**
```bash
python manage.py shell
```

```python
from employees.models import Employee
from django.contrib.auth.models import User

# Delete employees EMP001-EMP010
Employee.objects.filter(employee_no__startswith='EMP0').delete()

# Delete associated users
User.objects.filter(username__startswith='employee').delete()
```

### **Option 2: Django Admin**
1. Go to `http://127.0.0.1:8000/django-admin/`
2. Click "Employees" or "Users"
3. Select employees to delete
4. Choose "Delete selected" action

---

## 📊 Use Cases

### **1. Testing the UI Improvements:**
```bash
python manage.py seed_employees
# Now you have 10 employees to search, filter, and manage!
```

### **2. Testing Payroll Processing:**
- Create attendance records for seeded employees
- Run payroll for the period
- See how calculations work with real data

### **3. Demo/Presentation:**
- Show the system with realistic data
- No need to manually create test employees

### **4. Development:**
- Test features with multiple employees
- Verify search, filters, and pagination

---

## 🎯 Quick Start Workflow

```bash
# 1. Seed employees
python manage.py seed_employees

# 2. Start server
python manage.py runserver

# 3. Login as staff (create staff user first if needed)
# Go to: http://127.0.0.1:8000/accounts/login/

# 4. View employees
# Go to: http://127.0.0.1:8000/employees/

# 5. Try the search feature!
# Type "Juan" or "Accounting" in the search box
```

---

## 💡 Pro Tips

### **Create a Staff User to Manage Employees:**
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User, Group

# Create staff user
staff = User.objects.create_user(
    username='hr_staff',
    password='staff123',
    first_name='HR',
    last_name='Staff'
)

# Add to Staff group
staff_group, _ = Group.objects.get_or_create(name='Staff')
staff.groups.add(staff_group)

print("Staff user created: hr_staff / staff123")
```

### **Verify Seeded Data:**
```bash
python manage.py shell
```

```python
from employees.models import Employee

# Count employees
print(f"Total employees: {Employee.objects.count()}")

# List all
for emp in Employee.objects.all():
    print(f"{emp.employee_no}: {emp.last_name}, {emp.first_name} - {emp.department}")
```

---

## ⚠️ Important Notes

1. **Default password is weak** - Only for testing/development
2. **Change passwords in production** - Use strong passwords
3. **Safe to re-run** - Won't create duplicates
4. **Creates user accounts** - Each employee can login
5. **Random data** - Department/position combinations are random

---

## 🆘 Troubleshooting

### **Error: "No salary grades found"**
✅ **Solution:** The seeder automatically creates default salary grades

### **Error: "Employee already exists"**
✅ **Solution:** The seeder skips existing employees (safe to re-run)

### **Error: "User already exists"**
✅ **Solution:** Delete the user first or use different employee numbers

### **Want to start fresh?**
```bash
python manage.py flush  # ⚠️ Deletes ALL data!
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_employees
```

---

## 📝 File Location

```
employees/
  management/
    commands/
      seed_employees.py  ← The seeder command
```

---

**Happy Testing!** 🎉

Now you have 10 employees ready to test all the UI improvements we made!
