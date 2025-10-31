# Complete System Seeder Guide

## 🎉 **System Successfully Seeded!**

Your payroll system now has **14 months of realistic operational data** - simulating a company that's been running payroll for over a year!

---

## 📊 **What Was Created**

### **System Statistics:**
- 👥 **15 Employees** - Mix of departments and positions
- 💰 **8 Salary Grades** - From ₱15,000 to ₱60,000
- 📅 **4,507 Attendance Records** - 14 months of daily attendance
- 🏖️ **111 Leave Requests** - Sick, vacation, emergency leaves
- 💳 **14 Active Loans** - Various loan types with balances
- 📝 **12 Other Deductions** - Uniforms, parking, etc.
- 💰 **28 Payroll Runs** - Bi-monthly payroll for 14 months
- 📄 **405 Payslips** - Individual payslips for all runs

### **Payroll Status Breakdown:**
- 🔵 **DRAFT**: 0 (none pending)
- 🟡 **REVIEW**: 1 (recent payroll)
- 🟢 **APPROVED**: 1 (ready to process)
- 🟢 **PAID**: 26 (historical payrolls)

---

## 🔐 **Login Credentials**

### **Superuser (Full Access):**
```
URL: http://127.0.0.1:8000/django-admin/
Username: admin
Password: admin123
```

### **Staff/HR (Payroll Processing):**
```
URL: http://127.0.0.1:8000/accounts/login/
Username: hr_staff
Password: staff123
```

### **Employees (Self-Service):**
```
URL: http://127.0.0.1:8000/accounts/login/
Username: employee1, employee2, ..., employee15
Password: password123
```

---

## 👥 **Employee List**

| # | Name | Department | Position | Salary Grade |
|---|------|------------|----------|--------------|
| EMP001 | Juan Dela Cruz | Accounting | Senior Accountant | SG5 (₱35,000) |
| EMP002 | Maria Santos | HR | HR Manager | SG6 (₱40,000) |
| EMP003 | Jose Reyes | IT | IT Specialist | SG5 (₱35,000) |
| EMP004 | Ana Garcia | Sales | Sales Manager | SG6 (₱40,000) |
| EMP005 | Pedro Ramos | Operations | Operations Supervisor | SG5 (₱35,000) |
| EMP006 | Rosa Torres | Marketing | Marketing Coordinator | SG4 (₱30,000) |
| EMP007 | Carlos Flores | Accounting | Staff Accountant | SG3 (₱25,000) |
| EMP008 | Elena Mendoza | IT | Junior Developer | SG3 (₱25,000) |
| EMP009 | Miguel Castro | Sales | Sales Representative | SG3 (₱25,000) |
| EMP010 | Sofia Bautista | HR | HR Assistant | SG2 (₱20,000) |
| EMP011 | Ricardo Villanueva | Operations | Warehouse Staff | SG2 (₱20,000) |
| EMP012 | Carmen Aquino | Accounting | Accounting Clerk | SG2 (₱20,000) |
| EMP013 | Luis Fernandez | IT | IT Support | SG3 (₱25,000) |
| EMP014 | Isabella Morales | Marketing | Marketing Assistant | SG2 (₱20,000) |
| EMP015 | Gabriel Navarro | Sales | Sales Associate | SG2 (₱20,000) |

---

## 📅 **Historical Data Generated**

### **Attendance (14 Months)**
- **Daily records** from ~14 months ago to today
- **95% attendance rate** (realistic absences)
- **Regular hours**: 8 AM - 5 PM (with variations)
- **Occasional overtime**: 10% of days
- **Weekends excluded**: Only weekdays

### **Leave Requests**
- **2-5 leaves per employee** over the year
- **Types**: Sick, Vacation, Emergency, Personal
- **Statuses**: Mostly approved, some pending/rejected
- **Realistic dates**: Spread across 14 months

### **Loans (60% of employees)**
- **Types**: Salary Loan, Emergency Loan, Calamity Loan
- **Amounts**: ₱10,000 - ₱50,000
- **Monthly deductions**: ₱2,000 - ₱5,000
- **Balances decrease** over time as payments are made

### **Other Deductions (40% of employees)**
- **Uniform**: ₱500 (one-time)
- **ID Replacement**: ₱200 (one-time)
- **Parking Fee**: ₱500 (recurring)
- **Meal Deduction**: ₱1,000 (recurring)
- **Equipment Damage**: ₱1,500 (one-time)

### **Payroll Runs (Bi-Monthly)**
- **1st-15th** of each month
- **16th-end** of each month
- **Automatic status** based on age:
  - Recent runs: DRAFT or REVIEW
  - Last month: APPROVED
  - Older runs: PAID

---

## 🚀 **How to Use the Command**

### **Basic Usage:**
```bash
python manage.py seed_complete_system
```

### **Custom Number of Months:**
```bash
python manage.py seed_complete_system --months 24
```
This will generate 24 months (2 years) of data instead of 14.

### **Re-run Safely:**
The seeder is **idempotent** - it won't create duplicates:
- Skips existing employees
- Skips existing attendance records
- Skips existing payroll runs

---

## 🎯 **Test Scenarios You Can Now Explore**

### **1. View Historical Payroll**
```
Login as: hr_staff
Go to: http://127.0.0.1:8000/payroll/runs/
```
- See 28 payroll runs spanning 14 months
- Filter by status (PAID, APPROVED, REVIEW)
- Search by date or creator

### **2. Employee Attendance History**
```
Login as: hr_staff
Go to: http://127.0.0.1:8000/attendance/
```
- 4,500+ attendance records
- Search for specific employees
- View attendance patterns

### **3. Employee Self-Service**
```
Login as: employee1
Go to: http://127.0.0.1:8000/employee/
```
- View own payslips (14 months worth!)
- Check leave request history
- Download PDF payslips

### **4. Loan Management**
```
Login as: hr_staff
Go to: http://127.0.0.1:8000/payroll/loans/
```
- See 14 active loans
- Track remaining balances
- View monthly deductions

### **5. Leave Management**
```
Login as: hr_staff
Go to: http://127.0.0.1:8000/attendance/leaves/
```
- 111 leave requests
- Approve/reject pending leaves
- View leave history

---

## 💡 **UI Features to Test**

With all this data, you can now test:

### **Search Functionality** 🔍
- Search employees by name, department, position
- Search payroll runs by date
- Search attendance by employee

### **Status Badges** 🏷️
- See color-coded payroll statuses
- Active/inactive employee badges
- Leave request statuses

### **Confirmations** ⚠️
- Try deleting an employee (confirmation appears)
- Try marking payroll as paid (detailed warning)
- Try approving payroll (explains next steps)

### **Loading Indicators** ⏳
- Create new payroll run (spinner appears)
- Generate PDFs (processing message)

### **Pagination** 📄
- With 400+ payslips, test pagination
- With 4,500+ attendance records, test performance

---

## 📊 **Realistic Business Scenarios**

### **Scenario 1: Process Current Payroll**
1. Login as `hr_staff`
2. Go to Payroll Runs
3. Find the REVIEW status payroll
4. Review payslips
5. Approve it
6. Generate bank file
7. Mark as paid

### **Scenario 2: Check Employee Loan Balance**
1. Login as `hr_staff`
2. Go to Loans
3. See which employees have loans
4. Check remaining balances
5. Note: Balances decrease with each payroll!

### **Scenario 3: Employee Views Payslips**
1. Login as `employee1`
2. Go to My Payslips
3. See 14 months of payslips
4. Download PDF of any payslip
5. Check deposit status

### **Scenario 4: Approve Leave Request**
1. Login as `hr_staff`
2. Go to Leave Management
3. Find PENDING requests
4. Approve or reject
5. Employee can see updated status

---

## 🔧 **Customization Options**

### **Change Number of Employees:**
Edit `seed_complete_system.py`, line ~175:
```python
employees_data = [
    # Add more employees here
    ('New', 'Employee', 'Department', 'Position', 'SG3'),
]
```

### **Change Attendance Rate:**
Edit line ~280:
```python
if random.random() < 0.95:  # 95% attendance
    # Change to 0.90 for 90% attendance
```

### **Change Loan Percentage:**
Edit line ~350:
```python
employees_with_loans = random.sample(employees, int(len(employees) * 0.6))
# Change 0.6 to 0.8 for 80% of employees with loans
```

---

## 🗑️ **Reset Everything**

### **Option 1: Flush Database (Nuclear Option)**
```bash
python manage.py flush
```
⚠️ **Warning**: Deletes ALL data!

### **Option 2: Selective Delete**
```bash
python manage.py shell
```

```python
from payroll.models import PayrollRun, Payslip, Loan
from attendance.models import AttendanceLog, LeaveRequest
from employees.models import Employee

# Delete all payroll data
PayrollRun.objects.all().delete()
Payslip.objects.all().delete()
Loan.objects.all().delete()

# Delete attendance
AttendanceLog.objects.all().delete()
LeaveRequest.objects.all().delete()

# Delete employees (keeps users)
Employee.objects.all().delete()
```

Then re-run the seeder:
```bash
python manage.py seed_complete_system
```

---

## 📈 **Performance Notes**

### **Seeding Time:**
- **14 months**: ~30-60 seconds
- **24 months**: ~60-120 seconds
- **36 months**: ~120-180 seconds

### **Database Size:**
- **14 months**: ~5-10 MB
- **24 months**: ~10-20 MB
- **36 months**: ~20-30 MB

### **Records Generated:**
- **Attendance**: ~300 records per employee per month
- **Payroll Runs**: 2 per month
- **Payslips**: 15 per payroll run (one per employee)

---

## 🎓 **Learning Opportunities**

With this realistic data, you can:

1. **Test UI improvements** with real volume
2. **Practice payroll processing** workflows
3. **Understand data relationships** (employees → attendance → payslips)
4. **Test search and filtering** with large datasets
5. **Verify calculations** across multiple pay periods
6. **Test reporting** with historical data

---

## 🐛 **Troubleshooting**

### **Error: "Employee already exists"**
✅ **Solution**: The seeder skips existing employees. This is normal.

### **Error: "Payroll run already exists"**
✅ **Solution**: Delete existing payroll runs or use `--months` with different value.

### **Slow Performance**
✅ **Solution**: Reduce months: `--months 6` for faster seeding.

### **Want Fresh Start**
✅ **Solution**: Run `python manage.py flush` then re-seed.

---

## 🎉 **You're Ready!**

Your payroll system now has:
- ✅ **14 months of operational history**
- ✅ **Realistic employee data**
- ✅ **Complete payroll cycles**
- ✅ **Attendance tracking**
- ✅ **Loan management**
- ✅ **Leave requests**

**Start exploring:**
```
http://127.0.0.1:8000/
```

Login as `hr_staff` and see all the UI improvements in action with real data!

---

**Last Updated:** October 30, 2025  
**Command:** `python manage.py seed_complete_system`  
**Data Generated:** 14 months of payroll operations
