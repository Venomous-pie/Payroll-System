# Payroll System - Accountant's Quick Start Guide

## 👋 Welcome, Accountant!

This guide shows you **exactly** how to use the system as an accountant. No technical jargon!

---

## 📋 Your Daily/Monthly Tasks

### **FIRST TIME SETUP** (Do this once)

#### Step 1: Get Your Account
- Ask IT/Admin to create a **Staff** account for you
- You'll receive: Username & Password

#### Step 2: Login
1. Open browser: http://127.0.0.1:8000/
2. Enter your username
3. Enter your password
4. Click "Sign In"
5. You'll see the **Staff Dashboard**

---

## 📅 ROUTINE PAYROLL PROCESS

### **Every Day (5 minutes)**

#### Record Employee Attendance

**Where:** http://127.0.0.1:8000/attendance/

1. Click **"Attendance"** in the menu
2. Click **"Add Attendance"** button
3. Fill in:
   - **Employee**: Select from dropdown
   - **Date**: Today's date
   - **Time In**: e.g., 8:00 AM
   - **Time Out**: e.g., 5:00 PM
   - **Remarks**: (optional) Late, Overtime, etc.
4. Click **"Save"**
5. Repeat for all employees

**💡 Tip:** You can bulk import attendance from biometric if available.

---

### **Twice a Month (Payday - 30 minutes)**

#### Process Payroll (e.g., Every 15th and 30th)

**Where:** http://127.0.0.1:8000/payroll/runs/

#### **STEP 1: Create Payroll Run**

1. Click **"Payroll"** in menu
2. Click **"Create New Payroll Run"**
3. Enter dates:
   - **Period Start**: October 1, 2025
   - **Period End**: October 15, 2025
4. Click **"Create Payroll"** button

**⏳ Wait 10-30 seconds...**

The system automatically calculates:
- ✅ Basic salaries (based on attendance)
- ✅ Overtime pay
- ✅ SSS contributions
- ✅ PhilHealth contributions
- ✅ Pag-IBIG contributions
- ✅ Withholding tax
- ✅ Loan deductions
- ✅ Other deductions
- ✅ Net pay

You'll see: **"Payroll run created successfully! X payslips generated."**

---

#### **STEP 2: Review the Payroll**

1. You'll see a list of all employees and their payslips
2. Click on any employee to see details:
   - Gross Pay
   - Deductions breakdown
   - Net Pay
3. **Check for errors:**
   - Missing employees?
   - Wrong amounts?
   - Unusual deductions?

**If you see errors:**
- Note them down
- Contact IT if calculations seem wrong
- Check if employee attendance was recorded

**If everything looks good:**
- Continue to Step 3

---

#### **STEP 3: Change Status to "REVIEW"**

1. At the top of the payslip list, find the **Status** section
2. Select **"REVIEW"** from dropdown
3. Click **"Update Status"**

Status changes: **DRAFT** → **REVIEW**

---

#### **STEP 4: Get Manager Approval**

1. Ask your manager/supervisor to check the payroll
2. Manager reviews and changes status to **"APPROVED"**

Status changes: **REVIEW** → **APPROVED**

---

#### **STEP 5: Generate Documents**

Now you need 3 files for processing:

**A. Generate PDF Payslips** (For printing/emailing)
1. Click **"Generate All PDFs"** button
2. Wait 10-20 seconds
3. Success message appears
4. Each employee now has a PDF payslip

**B. Export to Excel** (For your records)
1. Click **"Export to Excel"** button
2. Excel file downloads automatically
3. Save it to your computer: `Payroll_Oct1-15_2025.xlsx`
4. Open in Excel to review/print

**C. Generate Bank File** (For salary transfer)
1. Click **"Generate Bank File"** button
2. CSV file downloads: `bank_transfer_1.csv`
3. Save it to your computer

---

#### **STEP 6: Process Bank Transfer**

1. Open your bank's online portal
2. Go to "Bulk Transfer" or "Payroll Upload"
3. Upload the `bank_transfer_1.csv` file
4. Review the list on bank portal
5. Authorize the transfer
6. Bank processes (usually same day or next day)

---

#### **STEP 7: Mark as Paid**

**After bank confirms money is sent:**

1. Go back to payroll system
2. Find your payroll run
3. Click **"Mark as Paid"** button
4. Click **"Confirm"**

Status changes: **APPROVED** → **PAID**

**🎉 Done! Payroll complete!**

The system automatically:
- ✅ Updates loan balances
- ✅ Records deposit date
- ✅ Marks payslips as deposited

---

## 📊 MONTHLY TASKS

### **Generate Reports for Government**

#### SSS Remittance Report
**Where:** http://127.0.0.1:8000/reports/

1. Click **"Reports"** menu
2. Select **"SSS Summary"**
3. Select month: October 2025
4. Click **"Generate"**
5. Print or save PDF

Shows:
- Total SSS contributions (employee + employer)
- Employee list with amounts
- Ready to submit to SSS

#### PhilHealth Report
Same as above, select **"PhilHealth Summary"**

#### Pag-IBIG Report
Same as above, select **"Pag-IBIG Summary"**

#### BIR Alphalist (Quarterly)
1. Click **"Reports"** → **"BIR Alphalist"**
2. Select quarter: Q4 2025
3. Generate Excel file
4. Use for quarterly tax filing

---

## 💰 MANAGE LOANS

### Add New Employee Loan

**Where:** http://127.0.0.1:8000/payroll/loans/

1. Click **"Payroll"** → **"Loans"**
2. Click **"Add New Loan"**
3. Fill in:
   - **Employee**: Select employee
   - **Loan Type**: Salary Loan / Emergency Loan / Housing
   - **Principal Amount**: ₱50,000.00
   - **Monthly Deduction**: ₱5,000.00
   - **Start Date**: November 1, 2025
4. Click **"Save"**

**System automatically:**
- Calculates remaining balance
- Deducts monthly amount from each payroll
- Marks loan as complete when paid

### View Active Loans
1. Click **"Payroll"** → **"Loans"**
2. See all active loans
3. Check remaining balances

---

## 🧾 OTHER DEDUCTIONS

### Add Uniform/Equipment Deduction

**Where:** http://127.0.0.1:8000/payroll/deductions/

1. Click **"Payroll"** → **"Other Deductions"**
2. Click **"Add Deduction"**
3. Fill in:
   - **Employee**: Select employee
   - **Description**: "Uniform cost"
   - **Amount**: ₱2,500.00
   - **Is Recurring**: 
     - ✅ Yes = Deduct every payroll
     - ❌ No = Deduct once only
4. Click **"Save"**

---

## 👥 MANAGE EMPLOYEES

### Add New Employee

**Where:** http://127.0.0.1:8000/employees/

1. Click **"Employees"** menu
2. Click **"Add Employee"**
3. Fill in all fields:
   - **Employee Number**: EMP001
   - **First Name**: Juan
   - **Last Name**: Dela Cruz
   - **Department**: Accounting
   - **Position**: Staff Accountant
   - **Salary Grade**: Select from dropdown
   - **Date Hired**: October 1, 2025
   - **Bank Name**: BDO
   - **Bank Account**: 0123456789
4. Click **"Save"**

### Update Employee Info
1. Go to **"Employees"** list
2. Click on employee name
3. Click **"Edit"**
4. Update information
5. Click **"Save"**

---

## 🔧 TROUBLESHOOTING

### "No payslips generated"
**Problem:** System says 0 payslips created

**Solutions:**
1. Check if employees have **Salary Grade** assigned
2. Check if **Attendance** was recorded for the period
3. Check if employees are marked **Active**
4. Ask IT to check contribution tables are set up

---

### "Wrong amount calculated"
**Problem:** Net pay seems incorrect

**Check:**
1. Is attendance correct?
2. Are there unexpected loans?
3. Are other deductions correct?
4. Click on payslip to see full breakdown

**Solution:** Contact IT if calculations are wrong

---

### "Can't download PDF"
**Problem:** PDF button doesn't work

**Solution:** Ask IT to check if ReportLab is installed

---

### "Excel file is blank"
**Problem:** Excel export has no data

**Solution:** 
1. Make sure payroll run has payslips
2. Refresh the page
3. Try again

---

## 📞 WHO TO CONTACT

### For System Issues:
- **IT Department** - Can't login, system errors, bugs

### For Payroll Questions:
- **HR Manager** - Employee information, policies
- **Your Supervisor** - Approval, clarifications

### For Government Contributions:
- **Admin** - Can update SSS/PhilHealth/Pag-IBIG rates

---

## ⚡ QUICK TIPS FOR ACCOUNTANTS

### 1. **Work in Batches**
- Record all attendance at once (end of day)
- Review all payslips together
- Generate all documents at once

### 2. **Double-Check Before "Paid"**
- Once marked "PAID", loan balances update
- Hard to reverse
- Always verify bank confirmation first

### 3. **Keep Excel Backups**
- Export to Excel for each payroll
- Save with clear filename: `Payroll_Oct1-15_2025.xlsx`
- Store in company backup folder

### 4. **Print Important Documents**
- Print 1 copy of payroll summary
- Keep for audit trail
- File chronologically

### 5. **Use the Search**
- In employee list, use search box
- Type employee name or number
- Faster than scrolling

### 6. **Check Before Deadline**
- Process payroll 2-3 days before payday
- Gives time to fix errors
- Bank transfers may take 1 day

### 7. **Regular Reports**
- Generate government reports monthly
- Don't wait until deadline
- Easier to reconcile monthly

---

## 📅 SUGGESTED SCHEDULE

### **Daily**
- 4:00 PM - Record attendance for all employees (5 min)

### **Every 13th and 28th** (2 days before payday)
- Create payroll run
- Review and verify
- Get approval
- Generate documents

### **Every 14th and 29th** (1 day before payday)
- Upload to bank
- Wait for confirmation

### **Every 15th and 30th** (Payday)
- Verify money deposited
- Mark as paid in system
- Done!

### **Monthly**
- 5th of next month - Generate SSS report
- 10th of next month - Generate PhilHealth report
- 10th of next month - Generate Pag-IBIG report

### **Quarterly**
- Generate BIR Alphalist

---

## ✅ CHECKLIST: Processing Payroll

Print this and check off each time:

```
PAYROLL FOR: Oct 1-15, 2025

□ Attendance recorded for all employees (14 days)
□ Created payroll run
□ Reviewed all payslips
□ No errors found
□ Status: DRAFT → REVIEW
□ Got manager approval
□ Status: REVIEW → APPROVED
□ Generated all PDFs
□ Exported to Excel (saved to folder)
□ Generated bank file (saved)
□ Uploaded to bank
□ Bank transfer authorized
□ Money deposited (confirmed)
□ Marked as PAID in system
□ Status: APPROVED → PAID
□ Filed documents
```

---

## 🎓 TRAINING EXERCISE

### Practice with Test Data:

1. **Add a test employee**
   - Name: Test Employee
   - Number: TEST001
   - Set salary grade

2. **Record attendance**
   - 5 days of attendance
   - Mix of 8-hour and 9-hour days

3. **Create test payroll**
   - Small date range
   - Just for test employee

4. **Review calculations**
   - Check if overtime calculated
   - Verify deductions

5. **Generate documents**
   - PDF, Excel, Bank file

6. **Delete test data**
   - Mark employee as inactive

---

## 🆘 EMERGENCY CONTACTS

**System is down?**
- Call IT: [xxx-xxxx]

**Payroll deadline but issue?**
- Call Supervisor: [xxx-xxxx]

**Bank transfer failed?**
- Call Bank: [xxx-xxxx]

---

**Remember:** The system does the math for you! Your job is to:
1. ✅ Enter accurate attendance
2. ✅ Review the calculations
3. ✅ Generate the documents
4. ✅ Process the payment

**You got this! 💪**

---

Last Updated: October 30, 2025

**Need more help?** Read the full `USER_GUIDE.md`
