
# 📘 Medical Invoice Comparison Tool — README.md

A lightweight, accurate, and audit-ready tool that compares **clinic invoices (PDF/Excel)** with the **doctor’s real work logs (Excel)** and automatically identifies **unpaid medical exams**.

Built for monthly financial reconciliation by clinics, physician groups, and healthcare audit teams.

---

## 🚀 1. Features

### ✔ Multi-source input
- One or more **PDF invoices**  
- One or more **Excel invoices**  
- One or more **Doctor Work Logs (Excel)**  
- Any combination supported — the tool merges everything automatically

### ✔ Intelligent data normalization
- Normalize patient names (remove accents, trim, case-insensitive)  
- Normalize exam names (e.g., *RX Tórax → rx torax*)  
- Normalize dates into **dd/mm/yyyy**  
- Detect mixed Latin-American date formats  
- Clean noisy text and strip punctuation

### ✔ Fuzzy matching engine
- Matches exams even if names differ  
- Examples:  
  - *“RX Tórax” ≈ “Rx Torax”*  
  - *“Eco Abd.” ≈ “Ecografía abdominal”*  
- Uses **RapidFuzz token_sort_ratio**  
- Multi-set logic: each invoice exam is matched only one time

### ✔ Accurate unpaid exam detection
- **Ground truth:** doctor’s real work logs  
- **Comparison:** clinic’s paid invoice(s)  
- Any exam performed but not billed → **UNPAID**

### ✔ Clean Excel output
The output Excel contains exactly:

| Nombre del paciente | Fecha (dd/mm/aaaa) | Descripción del examen |
|----------------------|---------------------|--------------------------|

### ✔ Correct chronological sorting
Sorted by:
1. **Month** (enero → diciembre)  
2. **Day**  
3. **Patient name**

### ✔ Multi-month support  
Upload invoices & logs from several months; the tool merges & sorts everything.

---

## 🛠 2. Installation

### Step 1 — Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

This installs:

- streamlit  
- pandas  
- pdfplumber  
- openpyxl  
- xlrd  
- unicodedata2  
- python-dateutil  
- rapidfuzz  
- tabula-py
- numpy
---

## ▶️ 3. Run the Application

Start the Streamlit app using:

```bash
streamlit run app.py
```

Your browser will open automatically.

---

## 📤 4. Using the App

### ① Upload PDF invoices  
- Supports multiple PDFs  
- Works with mixed table/text formats  
- Automatically extracts patient, date, exam

### ② Upload Excel invoices (optional)  
- Spanish & English headers supported  
- Automatically merged with PDF invoices

### ③ Upload Doctor Work Logs (required)  
- Multiple months supported  
- Treated as ground-truth performed exams

### ④ Click **Compare**

The tool:
- Normalizes all files  
- Applies fuzzy matching  
- Computes unpaid exams  
- Displays the result  
- Allows export as Excel

---

## 📄 5. Output Example

Based on your uploaded test file (*unpaid_exams.xlsx*):

```
Nombre del paciente     Fecha          Descripción del examen
------------------------------------------------------------------
Camila Nunez            02/01/2024     Eco Abd.
José Ángel Torres       02/01/2024     Tomografía axial
```

✔ Chronological  
✔ Alphabetical by patient  
✔ Only unpaid exams  
✔ Clean formatting  

---

## 🔍 6. Matching Logic (Overview)

### Grouping
- patient + date

### Exam comparison
- Fuzzy match each doctor exam against invoice exams  
- If threshold < 85 → unpaid  
- Each invoice exam can be matched **only once**

### Normalization
- Remove accents (tórax → torax)  
- Lowercase and trim  
- Remove punctuation  
- Convert dates with `dateutil.parser`  
- Support dd/mm and mm/dd formats  

### Sorting (performed in app.py)
```python
unpaid["date_dt"] = pd.to_datetime(unpaid["date"], dayfirst=True)
unpaid["month"]   = unpaid["date_dt"].dt.month
unpaid["day"]     = unpaid["date_dt"].dt.day

unpaid = unpaid.sort_values(["month", "day", "patient"])
unpaid = unpaid.drop(columns=["date_dt", "month", "day"])
```

---

## 🧪 7. Project Structure

```
/project
   app.py
   requirements.txt
   README.md
   INSTALLATION.md
   DEVELOPER_NOTES.md
   USER_GUIDE.md
   /modules
       pdf_reader.py
       excel_reader.py
       normalizer.py
       matcher.py
       exporter.py
```

---

## 🧩 8. Known Limitations
- Scanned PDFs without text may require OCR  
- Extremely irregular PDF formats may need manual adjustment  

---

## 🏁 9. Final Notes

This tool is:

- **Reliable** for monthly workflows  
- **Fast** even with large datasets  
- **Stable** across many file formats  
- **Accurate** thanks to RapidFuzz  
- **Audit-ready** (clean Excel output)

It fully satisfies the original functional requirements.
