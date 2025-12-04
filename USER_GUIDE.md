# USER GUIDE — Medical Invoice Comparison Tool
## Version 1.0 — Professional Edition

This document provides end-user instructions for operating the Medical Invoice Comparison Tool.  
It is intended for financial teams, administrative staff, and operational personnel responsible for verifying physician billing accuracy.

---

## 1. Purpose of the Tool

The tool compares:

- Clinic-paid invoices (PDF and/or Excel)
- Doctor’s real work logs (Excel)

The system identifies all medical examinations that were performed but not included in the clinic’s payment records.

The output is an Excel list used for reconciliation, payment verification, and audit processes.

---

## 2. Required Inputs

### 2.1. PDF Invoices (Optional)
The application accepts one or multiple PDF invoice files.  
Supported characteristics:
- Table-based invoices  
- Mixed text/table invoices  
- Multi-page documents

Extracted fields:
- Patient Name  
- Examination Date  
- Examination Description  
- Amount (if available)

### 2.2. Excel Invoices (Optional)
The application also accepts Excel versions of invoices.  
Common Spanish and English column names are automatically recognized.

### 2.3. Doctor Work Logs (Required)
The work logs represent the ground truth — what the doctor actually performed.

Characteristics:
- One or multiple Excel files  
- Any number of months  
- Files are merged automatically

---

## 3. How to Use the Application

### Step 1 — Launch the Interface
Run the following command:
```
streamlit run app.py
```
The tool loads in your default browser.

### Step 2 — Upload Files
Upload the necessary files in the following sections:

1. PDF Invoices  
2. Excel Invoices  
3. Doctor Work Logs (Mandatory)  

Multiple files may be uploaded for each category.

### Step 3 — Execute the Comparison
Click **Compare** to start processing.

The system will:
- Normalize patient names, dates, exam descriptions  
- Standardize dates to dd/mm/yyyy  
- Apply fuzzy matching  
- Identify unpaid examinations  
- Display results in the interface

### Step 4 — Export
Click **Download Unpaid Exams Excel** to export the official output file.

---

## 4. Output Format

The exported Excel file contains exactly three columns:

| Column Name            | Description                                        |
|------------------------|----------------------------------------------------|
| Nombre del paciente    | Patient name (normalized)                           |
| Fecha (dd/mm/aaaa)     | Exam date in dd/mm/yyyy format                      |
| Descripción del examen | Exam description (normalized)                       |

Only unpaid exams appear in the output.

---

## 5. Sorting Logic

The final report is sorted by:
1. Month (January → December)
2. Day
3. Patient Name (alphabetical)

---

## 6. Multi-Month Processing

The tool supports processing multiple months at once.  
Upload any mix of:
- Monthly PDF invoices  
- Excel invoices  
- Doctor work logs  

All files are merged and analyzed in a unified process.

---

## 7. Example Output

```
Nombre del paciente     Fecha          Descripción del examen
------------------------------------------------------------------
Camila Nunez            02/01/2024     Eco Abd.
José Ángel Torres       02/01/2024     Tomografía axial
```

---

## 8. Operational Notes

- Scanned PDFs without text may require OCR.  
- Highly irregular invoice layouts may require manual review.  
- The date parser automatically resolves ambiguous Latin-American formats.

---

# End of User Guide
