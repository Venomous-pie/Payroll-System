# Payroll System - User Guide for Accountants & HR Staff

## 🎯 Overview
This is a **user-friendly web interface** for managing payroll. No technical knowledge required!

---

## 🔐 Getting Started

### Login
1. Go to: http://127.0.0.1:8000/
2. Enter your username and password
3. You'll be redirected based on your role:
   - **Admin** → Admin Dashboard
   - **Staff/HR** → Staff Dashboard
   - **Employee** → Employee Dashboard

---

## 👥 User Roles

### **Admin** (Full Access)
- Manage all system settings
- Manage users and roles
- Access Django admin panel

### **Staff/HR** (Payroll Processors)
- Process payroll
- Manage employees
- Generate reports
- Handle loans and deductions
- Export bank files

### **Employee** (Self-Service)
- View own payslips
- Download PDF payslips
- Check salary deposit status
- View salary information

---

## 📋 Main Features

### For Staff/HR Personnel:

#### 1. **Employee Management**
**URL:** http://127.0.0.1:8000/employees/

- ✅ Add new employees
- ✅ Update employee information
- ✅ Manage bank account details
- ✅ Set salary grades
- ✅ Activate/deactivate employees

**Steps to Add Employee:**
1. Click "Employees" in navigation
2. Click "Add Employee" button
3. Fill in:
   - Employee Number
   - Name
   - Department
   - Position
   - Salary Grade
   - Bank Details
4. Click "Save"

---

#### 2. **Process Payroll** (Main Feature)
**URL:** http://127.0.0.1:8000/payroll/runs/

**Step-by-Step Process:**

**Step 1: Create Payroll Run**
1. Go to **Payroll** → **Create New Run**
2. Select:
   - Period Start Date (e.g., Oct 1, 2025)
   - Period End Date (e.g., Oct 15, 2025)
3. Click **"Create Payroll"**
4. System automatically calculates:
   - ✅ Basic pay based on attendance
   - ✅ Overtime pay
   - ✅ SSS contributions
   - ✅ PhilHealth contributions
   - ✅ Pag-IBIG contributions
   - ✅ Withholding tax
   - ✅ Loan deductions
   - ✅ Other deductions
   - ✅ Net pay

**Step 2: Review Payroll**
1. Check all payslips for accuracy
2. Verify calculations
3. Click **"Move to Review"** status

**Step 3: Approve Payroll**
1. After review, click **"Approve"**
2. Status changes to APPROVED

**Step 4: Generate Documents**
- **Generate PDFs**: Click "Generate All PDFs" button
  - Creates printable payslips for all employees
- **Export to Excel**: Click "Export Excel" button
  - Downloads complete payroll spreadsheet
- **Bank File**: Click "Generate Bank File" button
  - Downloads CSV file for bank transfer

**Step 5: Process Payment**
1. Upload bank file to your bank's portal
2. After salaries are deposited, click **"Mark as Paid"**
3. Status changes to PAID
4. Loan balances automatically updated

---

#### 3. **Manage Loans**
**URL:** http://127.0.0.1:8000/payroll/loans/

- View all active employee loans
- Track remaining balances
- Monthly deductions automatically applied during payroll

---

#### 4. **Manage Deductions**
**URL:** http://127.0.0.1:8000/payroll/deductions/

- Add uniform costs
- Add equipment charges
- Set recurring or one-time deductions

---

#### 5. **Attendance Management**
**URL:** http://127.0.0.1:8000/attendance/

- Record employee time in/out
- Manage leave requests
- Approve/reject leaves

---

### For Employees:

#### 1. **View Payslips**
**URL:** http://127.0.0.1:8000/payroll/my/payslips/

- See all your payslips
- View detailed breakdown
- Download PDF copies

#### 2. **Download Payslip**
1. Click on any payslip
2. Click "Download PDF" button
3. Save or print your payslip

#### 3. **Check Salary Status**
**URL:** http://127.0.0.1:8000/payroll/my/deposits/

- See if salary has been deposited
- View deposit dates
- Check payment history

---

## 🔧 System Settings (Admin Only)

### Government Contribution Tables
**URL:** http://127.0.0.1:8000/django-admin/contributions/

Update when government rates change:

1. **SSS Contributions**
   - Add salary brackets
   - Set employee/employer shares
   
2. **PhilHealth**
   - Update premium rate (currently 5%)
   - Set maximum contribution cap
   
3. **Pag-IBIG**
   - Update employee rate (2%)
   - Update employer rate (2%)
   - Set maximum contributions
   
4. **BIR Tax Tables**
   - Add tax brackets
   - Set base tax and rates

---

## 📊 Reports Available

### 1. **Payroll Summary**
- Total employees paid
- Total gross pay
- Total deductions
- Total net pay
- Breakdown by department

### 2. **Bank Transfer Report**
- List of employees to be paid
- Account numbers
- Amounts
- Bank-wise breakdown

### 3. **Government Contributions**
- SSS summary
- PhilHealth summary
- Pag-IBIG summary
- For monthly remittance

---

## ⚠️ Common Issues & Solutions

### "No employee record found"
**Solution:** Staff must first create an employee record linked to your user account.

### "Could not calculate payroll"
**Causes:**
- Missing salary grade
- Missing contribution tables
- No attendance records

**Solution:**
1. Check employee has salary grade assigned
2. Verify government contribution tables are set up
3. Ensure attendance is recorded

### "PDF generation failed"
**Solution:** 
- Check if `media/payslips/` folder exists
- Verify ReportLab is installed

---

## 💡 Best Practices

### For Accurate Payroll:
1. ✅ Record attendance daily
2. ✅ Update employee information immediately when changed
3. ✅ Review payroll before approval
4. ✅ Keep contribution tables updated
5. ✅ Backup data regularly

### Payroll Processing Schedule:
- **Day 1-14**: Record attendance
- **Day 15**: Create payroll run
- **Day 16**: Review calculations
- **Day 17**: Approve payroll
- **Day 18**: Generate documents and send to bank
- **Day 20**: Mark as paid after bank confirmation

---

## 📞 Support

### Technical Issues:
- Contact IT Department
- Check `IMPLEMENTATION_SUMMARY.md` for developer docs

### Payroll Questions:
- Contact HR Manager
- Refer to company payroll policy

---

## 🎓 Quick Training Checklist

### For New HR Staff:
- [ ] Login and navigate the system
- [ ] Add a test employee
- [ ] Create a salary grade
- [ ] Record attendance
- [ ] Process a test payroll run
- [ ] Generate PDF payslips
- [ ] Export to Excel
- [ ] Generate bank file
- [ ] Understand workflow: DRAFT → REVIEW → APPROVED → PAID

### For Employees:
- [ ] Login to system
- [ ] View your payslips
- [ ] Download a PDF payslip
- [ ] Check deposit status

---

## 📱 Mobile Access

The system is web-based and responsive. You can access it from:
- Desktop computers
- Tablets
- Mobile phones (use landscape mode for better view)

---

## 🔒 Security Reminders

- ✅ Never share your password
- ✅ Logout when finished
- ✅ Use strong passwords
- ✅ Report suspicious activity
- ✅ Only access from company network

---

Last Updated: October 30, 2025

**For technical documentation, see:** `IMPLEMENTATION_SUMMARY.md`
