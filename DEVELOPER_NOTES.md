# DEVELOPER NOTES — Medical Invoice Comparison Tool
## Technical Documentation — Professional Edition

This document describes the internal architecture, data flow, normalization rules, and matching algorithms used in the tool.  
It is intended for engineers enhancing, debugging, or extending the system.

---

## 1. System Architecture

The application is structured into modular components:

```
PDF/Excel Inputs
        ↓
pdf_reader.py       → PDF extraction  
excel_reader.py     → Excel extraction  
        ↓
normalizer.py       → Text + date normalization  
        ↓
matcher.py          → Fuzzy matching + unpaid detection  
        ↓
app.py              → UI, orchestration, sorting  
        ↓
exporter.py         → Excel output generation
```

Each module is independent and returns standardized pandas DataFrames.

---

## 2. Module-Level Documentation

### 2.1 pdf_reader.py

Purpose:  
Extract tabular invoice data from PDF files.

Key capabilities:
- Supports UploadedFile, file-like objects, raw bytes  
- Uses pdfplumber for table extraction  
- Processes multi-page and multi-file inputs  
- Handles irregular row lengths (padding/trimming)  
- Maps Spanish/English headers to internal schema  
- Returns unified DataFrame

---

### 2.2 excel_reader.py

Purpose:  
Reads Excel invoices and work logs.

Features:
- Header auto-detection  
- Spanish/English column name support  
- Enforces required fields:
  - patient  
  - date  
  - exam  
- Produces validated DataFrames

---

### 2.3 normalizer.py

Purpose:  
Centralized normalization of text and dates.

Rules include:
- Accent removal (tórax → torax)  
- Lowercasing  
- Whitespace trimming  
- Punctuation cleanup  
- Collapsing duplicate spaces  
- Date parsing via dateutil  
- Output date format: dd/mm/yyyy

---

### 2.4 matcher.py

Purpose:  
Determine which doctor exams are unpaid.

Algorithm Summary:
1. Group data by (patient, date)  
2. For each doctor exam:
   - Compute fuzzy similarity (RapidFuzz token_sort_ratio)  
   - If score < threshold → unpaid  
   - Otherwise, matched invoice exam is removed (consumed)
3. Return all unmatched exams  
4. Note: sorting is not performed here (handled by app.py)

Key properties:
- Multi-set matching  
- Unpaid detection based on ground truth (doctor logs)

---

### 2.5 app.py

Purpose:  
Main orchestrator + Streamlit UI.

Responsibilities:
- Handle all file uploads  
- Trigger module execution in correct order  
- Merge multiple invoices/logs  
- Apply final sorting (month → day → patient)  
- Manage export process and table display

---

### 2.6 exporter.py

Purpose:  
Generate final unpaid Excel report.

Output columns:
- Nombre del paciente  
- Fecha (dd/mm/aaaa)  
- Descripción del examen  

Ensures export consistency and formatting.

---

## 3. Extendability

Developers may extend:
- PDF parsing (OCR, new layouts)  
- Matching and scoring rules  
- Additional normalization for other languages  
- Extra processing steps (validation, analytics)

---

## 4. Maintenance Guidelines

- Avoid modifying normalization without updating tests  
- Keep fuzzy threshold stable  
- Maintain module boundaries  
- Ensure DataFrames remain clean and well-typed  
- Sorting should remain in app.py

---

# End of Developer Notes
