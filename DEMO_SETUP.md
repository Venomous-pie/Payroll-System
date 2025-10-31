# 🚀 Payroll System - Demo Setup Guide

## Quick Start (One-Click Setup)

### **For Demo/Presentation:**

Simply **double-click** this file:
```
setup_demo.bat
```

That's it! The script will:
1. ✅ Delete old database
2. ✅ Create fresh database with migrations
3. ✅ Seed 14 months of realistic data
4. ✅ Start the development server
5. ✅ Open your browser automatically

---

## What Gets Created

### **📊 System Data:**
- 👥 **15 Employees** (various departments & positions)
- 💰 **8 Salary Grades** (₱15K - ₱60K)
- 📅 **4,500+ Attendance Records** (14 months)
- 🏖️ **150+ Leave Requests**
- 💳 **Active Loans** with balances
- 📝 **Other Deductions**
- 💰 **27 Payroll Runs** (bi-monthly)
- 📄 **400+ Payslips**

### **🔐 Login Accounts:**

| Role | Username | Password | URL |
|------|----------|----------|-----|
| **Superuser** | admin | admin123 | http://127.0.0.1:8000/django-admin/ |
| **HR Staff** | hr_staff | staff123 | http://127.0.0.1:8000/accounts/login/ |
| **Employees** | employee1-15 | password123 | http://127.0.0.1:8000/accounts/login/ |

---

## Demo Workflow

### **Scenario 1: Process Current Payroll (5 minutes)**

1. **Login as HR Staff:**
   - URL: http://127.0.0.1:8000/accounts/login/
   - Username: `hr_staff`
   - Password: `staff123`

2. **Go to Payroll Runs:**
   - Click "Payroll" in navigation
   - See 27 historical payroll runs

3. **Find REVIEW Status Payroll:**
   - Look for the 🟡 **REVIEW** badge
   - Click "View Payslips"

4. **Review Payslips:**
   - 🔍 Use search to find specific employees
   - See totals at bottom of table
   - Check all amounts are correct

5. **Approve Payroll:**
   - Click "✓ Approve Payroll" button
   - See confirmation dialog
   - Click "OK"
   - Status changes to 🟢 **APPROVED**

6. **Generate Bank File:**
   - Click "🏦 Bank File" button
   - CSV file downloads automatically
   - Open to see bank transfer details

7. **Mark as Paid:**
   - Click "💰 Mark as Paid"
   - Check confirmation checkbox
   - Click "Yes, Mark as Deposited"
   - Status changes to 🟢 **PAID**
   - Loan balances automatically updated!

---

### **Scenario 2: Employee Self-Service (2 minutes)**

1. **Login as Employee:**
   - URL: http://127.0.0.1:8000/accounts/login/
   - Username: `employee1`
   - Password: `password123`

2. **View Payslips:**
   - See 14 months of payslip history
   - Click any payslip to view details
   - Download PDF (if implemented)

3. **Check Deposit Status:**
   - See which payslips have been deposited
   - View deposit dates

---

### **Scenario 3: Manage Employees (3 minutes)**

1. **Login as HR Staff**

2. **Go to Employees:**
   - Click "Employees" in navigation
   - See all 15 employees

3. **Search Functionality:**
   - Type "Juan" in search box
   - Results filter instantly
   - Try searching by department: "Accounting"

4. **View Employee Details:**
   - Click on any employee
   - See salary grade, position, bank details
   - View hire date and status

5. **Edit Employee:**
   - Click "Edit" button
   - See improved form with tooltips
   - Hover over (?) icons for help
   - Cancel to go back

---

### **Scenario 4: View Historical Data (2 minutes)**

1. **Login as HR Staff**

2. **View Attendance:**
   - Go to Attendance section
   - See 4,500+ attendance records
   - Search by employee name
   - Filter by date range

3. **View Leave Requests:**
   - Go to Leave Management
   - See approved, pending, rejected leaves
   - Approve/reject pending requests

4. **View Loans:**
   - Go to Loan Management
   - See active loans with balances
   - Note: Balances decrease with each payroll!

---

## UI Features to Highlight

### **🔍 Search Functionality:**
- Instant filtering on employee lists
- Search payroll runs by date
- Find specific attendance records

### **🏷️ Status Badges:**
- Color-coded payroll statuses
- Active/Inactive employee indicators
- Leave request statuses

### **⚠️ Confirmation Dialogs:**
- Approve payroll (explains next steps)
- Delete actions (warns about consequences)
- Mark as paid (requires checkbox confirmation)

### **⏳ Loading Indicators:**
- Spinner appears during processing
- Button disables to prevent double-clicks
- "Processing..." message shown

### **💡 Tooltips & Help:**
- Hover over (?) icons for explanations
- Contextual help on forms
- Next steps guidance

### **📊 Totals & Summaries:**
- Payslip totals at bottom of table
- Employee count in headers
- Financial summaries

---

## Troubleshooting

### **Script Fails to Run:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Run manually:
python manage.py migrate
python manage.py seed_complete_system --months 14
python manage.py runserver
```

### **Port Already in Use:**
```bash
# Use different port:
python manage.py runserver 8080
```

### **Want Fresh Start:**
```bash
# Just run the script again!
setup_demo.bat
```

---

## Manual Setup (If Needed)

If the batch script doesn't work, run these commands manually:

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Delete database
del db.sqlite3

# 3. Run migrations
python manage.py migrate

# 4. Seed data
python manage.py seed_complete_system --months 14

# 5. Start server
python manage.py runserver

# 6. Open browser
start http://127.0.0.1:8000
```

---

## Customization

### **Change Number of Months:**
```bash
# 6 months of data (faster)
python manage.py seed_complete_system --months 6

# 24 months of data (more history)
python manage.py seed_complete_system --months 24
```

### **Add More Employees:**
Edit `employees/management/commands/seed_complete_system.py` line ~175

---

## Demo Tips

### **Before the Demo:**
1. ✅ Run `setup_demo.bat` (takes 60 seconds)
2. ✅ Test login as `hr_staff`
3. ✅ Bookmark key URLs
4. ✅ Close unnecessary browser tabs
5. ✅ Set zoom to 100% for better visibility

### **During the Demo:**
1. 🎯 Start with employee self-service (relatable)
2. 🎯 Show search functionality (impressive)
3. 🎯 Process a payroll end-to-end (core feature)
4. 🎯 Highlight confirmations and safety features
5. 🎯 Show historical data (proves it's production-ready)

### **Key Talking Points:**
- ✨ "14 months of operational history"
- ✨ "Automatic loan balance updates"
- ✨ "Bi-monthly payroll processing"
- ✨ "Bank file generation for transfers"
- ✨ "Employee self-service portal"
- ✨ "Comprehensive audit trail"

---

## System Requirements

- ✅ Windows 10/11
- ✅ Python 3.8+
- ✅ Virtual environment activated
- ✅ All dependencies installed (`pip install -r requirements.txt`)

---

## Support

If you encounter any issues:
1. Check the console output for errors
2. Verify virtual environment is activated
3. Ensure all dependencies are installed
4. Try running commands manually (see above)

---

**Last Updated:** October 30, 2025  
**Setup Time:** ~60 seconds  
**Demo Duration:** 10-15 minutes  
**Wow Factor:** 🚀🚀🚀

---

## Quick Reference Card (Print This!)

```
┌─────────────────────────────────────────────────────────┐
│         PAYROLL SYSTEM - DEMO QUICK REFERENCE           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🚀 START DEMO:  Double-click setup_demo.bat           │
│                                                         │
│  🔐 HR LOGIN:    hr_staff / staff123                   │
│  🔐 EMPLOYEE:    employee1 / password123               │
│  🔐 ADMIN:       admin / admin123                      │
│                                                         │
│  📊 DATA:        15 employees, 14 months history       │
│  💰 PAYROLLS:    27 runs (bi-monthly)                  │
│  📄 PAYSLIPS:    400+ generated                        │
│                                                         │
│  🎯 DEMO FLOW:                                         │
│     1. Login as hr_staff                               │
│     2. View Payroll Runs                               │
│     3. Approve REVIEW status payroll                   │
│     4. Generate Bank File                              │
│     5. Mark as Paid                                    │
│     6. Show employee self-service                      │
│                                                         │
│  ⚡ FEATURES TO HIGHLIGHT:                             │
│     • Instant search                                   │
│     • Status badges                                    │
│     • Confirmation dialogs                             │
│     • Automatic calculations                           │
│     • Loan balance updates                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Print this card and keep it handy during demos!** 📋
