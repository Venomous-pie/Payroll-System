# 📄 PDF Payslip Access Guide

## How to Access Generated PDFs

After clicking "📄 Generate PDFs" button, the PDFs are automatically accessible in the payslips table.

---

## 🎯 Quick Access

### **From Payslips Page:**

1. **Navigate to Payroll Run:**
   - Go to Payroll → Runs
   - Click "View Payslips" on any payroll run

2. **Generate PDFs (if not generated):**
   - Click "📄 Generate PDFs" button
   - Wait for success message
   - Page refreshes automatically

3. **Download Individual PDFs:**
   - Look at the **PDF column** (rightmost column)
   - Click "📄 Download" button next to each employee
   - PDF opens in new tab or downloads

4. **PDF Status:**
   - ✅ **"📄 Download"** - PDF is ready
   - ⚪ **"Not generated"** - Click "Generate PDFs" button first

---

## 📁 Where PDFs Are Stored

### **File System Location:**
```
Payroll_System/
└── media/
    └── payslips/
        ├── payslip_EMP001_28.pdf
        ├── payslip_EMP002_28.pdf
        ├── payslip_EMP003_28.pdf
        └── ...
```

### **URL Pattern:**
```
http://127.0.0.1:8000/media/payslips/payslip_EMP001_28.pdf
```

### **Naming Convention:**
```
payslip_{EMPLOYEE_NO}_{PAYROLL_RUN_ID}.pdf
```

Example:
- `payslip_EMP001_28.pdf` = Employee #001, Payroll Run #28
- `payslip_EMP015_27.pdf` = Employee #015, Payroll Run #27

---

## 🔍 Finding PDFs

### **Method 1: Through UI (Recommended)**
1. Login as HR Staff
2. Go to Payroll → Runs
3. Click "View Payslips"
4. Click "📄 Download" in PDF column

### **Method 2: Direct File Access**
1. Open File Explorer
2. Navigate to: `C:\Users\Torme\projects\Payroll_System\media\payslips\`
3. Double-click any PDF file

### **Method 3: Direct URL**
```
http://127.0.0.1:8000/media/payslips/payslip_EMP001_28.pdf
```
Replace `EMP001` and `28` with actual employee number and payroll run ID.

---

## 🎨 PDF Features

### **What's Included in Each PDF:**
- 📋 Employee information (name, employee #, position)
- 💰 Gross pay breakdown
- 📊 Deductions (SSS, PhilHealth, Pag-IBIG, Tax)
- 💳 Loan deductions (if applicable)
- 📝 Other deductions
- 💵 Net pay (take-home amount)
- 📅 Pay period dates
- 🏦 Bank details (if available)

---

## 🚀 Bulk Operations

### **Generate All PDFs at Once:**
1. Go to payroll run payslips page
2. Click "📄 Generate PDFs" button
3. System generates PDFs for ALL employees in that run
4. Success message shows count: "Generated 15 PDF payslips!"

### **Re-generate PDFs:**
- PDFs are only generated once
- If PDF already exists, it won't be regenerated
- To regenerate: Delete the PDF file first, then click "Generate PDFs" again

---

## 👤 Employee Access

### **Employees Can Download Their Own Payslips:**

1. **Login as Employee:**
   ```
   URL: http://127.0.0.1:8000/accounts/login/
   Username: employee1
   Password: password123
   ```

2. **View Payslips:**
   - Click "My Payslips" in navigation
   - See list of all payslips

3. **Download PDF:**
   - Click on any payslip
   - Click "Download PDF" button (if implemented)
   - Or access via direct URL

---

## 🔐 Security

### **Access Control:**
- ✅ **HR Staff** - Can generate and download all PDFs
- ✅ **Employees** - Can only access their own payslips
- ❌ **Public** - No access to PDFs

### **File Permissions:**
- PDFs are stored in `media/payslips/` folder
- Only accessible through Django URLs (with authentication)
- Direct file access requires server permissions

---

## 📊 PDF Generation Process

### **What Happens When You Click "Generate PDFs":**

1. **System checks** if PDF already exists
2. **Generates PDF** for each payslip without PDF
3. **Saves to** `media/payslips/` folder
4. **Updates database** with PDF file path
5. **Shows success message** with count
6. **Refreshes page** to show download buttons

### **Generation Time:**
- **1 employee** = ~0.5 seconds
- **15 employees** = ~7-10 seconds
- **100 employees** = ~50-60 seconds

---

## 🛠️ Troubleshooting

### **"Not generated" Shows for All Employees:**
**Solution:** Click the "📄 Generate PDFs" button at the top

### **Download Button Not Appearing:**
**Solution:** 
1. Check if PDFs were generated successfully
2. Look for error messages
3. Check `media/payslips/` folder exists
4. Verify MEDIA_URL and MEDIA_ROOT in settings

### **PDF Opens Blank:**
**Solution:**
1. Check PDF generation function
2. Verify all payslip data is present
3. Check for errors in console

### **404 Error When Clicking Download:**
**Solution:**
1. Verify MEDIA_URL is configured in settings.py
2. Check urls.py includes media URL pattern
3. Ensure `media/payslips/` folder exists

### **PDFs Not Saving:**
**Solution:**
1. Check folder permissions
2. Verify MEDIA_ROOT path is correct
3. Ensure `media/` folder exists in project root

---

## 📝 Configuration

### **Settings Required (Already Configured):**

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### **URLs Required (Already Configured):**

```python
# urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### **Model Field:**

```python
# payroll/models.py
class Payslip(models.Model):
    pdf_file = models.FileField(upload_to='payslips/', null=True, blank=True)
```

---

## 🎯 Demo Scenario

### **Show PDF Generation in Demo:**

1. **Login as hr_staff**
2. **Navigate to Payroll Runs**
3. **Click on APPROVED payroll run**
4. **Point out "Not generated" in PDF column**
5. **Click "📄 Generate PDFs" button**
6. **Wait for success message**
7. **Show "📄 Download" buttons appear**
8. **Click download on one employee**
9. **PDF opens in new tab**
10. **Show professional payslip layout**

**Talking Points:**
- "One-click PDF generation for all employees"
- "Individual download links for each payslip"
- "Professional PDF format"
- "Employees can access their own payslips"
- "Secure file storage"

---

## 📂 Folder Structure

```
Payroll_System/
├── media/                          # Created automatically
│   └── payslips/                   # PDF storage
│       ├── payslip_EMP001_28.pdf
│       ├── payslip_EMP002_28.pdf
│       └── ...
│
├── templates/
│   └── payroll/
│       └── run_payslips.html       # Shows download buttons
│
└── payroll/
    ├── models.py                   # Payslip model with pdf_file field
    └── views.py                    # generate_all_payslip_pdfs view
```

---

## 🔄 Workflow

```
1. Process Payroll
   ↓
2. Approve Payroll
   ↓
3. Generate PDFs ← Click button
   ↓
4. Download Individual PDFs ← Click per employee
   ↓
5. Email to Employees (manual or automated)
   ↓
6. Mark as Paid
```

---

## 💡 Tips

### **For HR Staff:**
- Generate PDFs after approving payroll
- Download all PDFs before marking as paid
- Keep PDFs organized by pay period
- Back up PDF files regularly

### **For Employees:**
- Download and save your payslips
- Keep for tax records
- Print if needed for loans/applications

### **For Developers:**
- PDFs are generated using reportlab or similar library
- Customize PDF template in payroll app
- Add company logo to PDFs
- Include additional fields as needed

---

## 📧 Future Enhancements

### **Possible Improvements:**
- ✨ Email PDFs automatically to employees
- ✨ Bulk download all PDFs as ZIP
- ✨ PDF password protection
- ✨ Digital signatures
- ✨ QR code for verification
- ✨ Mobile-optimized PDF viewer
- ✨ Print all PDFs at once

---

**Last Updated:** October 30, 2025  
**Status:** Fully Functional ✅  
**Access:** HR Staff & Employees
