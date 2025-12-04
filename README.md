# Medical Invoice Comparison Tool – Prototip / Prototype  
(Bilingual README – Türkçe & English)

---

# 🇺🇸 English Version

## ⭐ Project Overview  
This prototype was developed to explore automated validation of medical billing data and to analyze the requirements of real-world medical invoice reconciliation tasks. The system compares clinic invoices (PDF/Excel) with a doctor’s work logs to detect missing or unpaid medical procedures.

A fully artificial multilingual dataset (Spanish, French, English) was created to avoid using real patient information. The dataset includes accented characters, mixed date formats, and varied medical procedure descriptions. Spanish column names in the Excel output intentionally reflect Latin American billing formats.

---

## ⭐ Key Features  
- Read invoices from **PDF (layout-based parsing)** and **Excel files**  
- Process multilingual patient names and procedure descriptions  
- Normalize text with **Unicode NFKD**, accent removal, and cleanup  
- Apply **fuzzy matching (RapidFuzz)** to detect equivalent procedures  
- Compare doctor logs vs. billed procedures  
- Sort results **chronologically** (Year → Month → Day → Patient)  
- Export missing/unpaid procedures as a **clean Excel report**  

---

## ⭐ Technical Architecture  
### **PDF Extraction**
- Performed using **pdfplumber**  
- Layout-based table detection (no OCR)
- Geometry-driven row/column reconstruction

### **Normalization (NLP Preprocessing)**
- Unicode NFKD  
- Accent removal  
- Whitespace + punctuation cleanup  
- Lowercasing  
- Multilingual handling (ES/FR/EN)

### **Matching Logic**
- Deterministic grouping (patient + date)  
- Fuzzy similarity scoring for procedure names (RapidFuzz)  
- Threshold-based matching for abbreviations vs. full terms  

### **Data Workflow**
1. Load datasets  
2. Extract tables from PDFs  
3. Normalize columns  
4. Clean & standardize records  
5. Fuzzy match procedures  
6. Identify unpaid/missing records  
7. Sort chronologically  
8. Export Excel report  

---

## ⭐ Output  
The tool generates a minimal and finance-friendly Excel file containing only:  
- Patient name  
- Date (dd/mm/yyyy)  
- Procedure description  

Intentionally minimal to support real audit workflows.

---

# 🇹🇷 Türkçe Versiyon

## ⭐ Proje Özeti  
Bu prototip, tıbbi fatura verilerinin otomatik doğrulanmasını incelemek ve gerçek hayattaki fatura–doktor kaydı uzlaştırma süreçlerinin gereksinimlerini analiz etmek için geliştirildi. Sistem; PDF/Excel faturaları doktorun çalışma kayıtlarıyla karşılaştırarak **eksik veya faturalandırılmamış işlemleri tespit eder**.

Gerçek hasta verisi kullanmamak için; aksanlı karakterler, farklı tarih biçimleri ve çeşitli işlem adları içeren tamamen yapay ve çok dilli bir veri seti (İspanyolca/Fransızca/İngilizce) oluşturuldu. Excel çıktısındaki İspanyolca kolon adları kasıtlıdır.

---

## ⭐ Temel Özellikler  
- **PDF (layout analizi) ve Excel**’den fatura okuma  
- Çok dilli isim ve işlem açıklamalarını işleme  
- NLP tabanlı metin normalizasyonu (Unicode NFKD)  
- **RapidFuzz bulanık eşleştirme** ile benzer işlemlerin tespiti  
- Doktor kaydı vs. fatura karşılaştırma  
- **Yıl → Ay → Gün → Hasta** sırasına göre kronolojik sıralama  
- Sadece **ödenmemiş işlemleri** içeren Excel raporu oluşturma  

---

## ⭐ Teknik Mimari  
### **PDF Ayrıştırma**
- **pdfplumber** ile OCR’siz tablo çıkarımı  
- Layout analizi  
- Geometri tabanlı satır/sütun yeniden yapılandırması  

### **Normalizasyon (NLP)**
- Unicode NFKD  
- Aksan temizleme  
- Boşluk ve noktalama temizliği  
- Küçük harfe dönüştürme  

### **Eşleştirme Mantığı**
- Deterministic grouping (hasta + tarih)  
- RapidFuzz benzerlik skoru  
- Kısaltma vs. tam yazım eşleştirmesi  

---

## ⭐ Veri İşleme Akışı  
1. Veri yükleme  
2. PDF’den tablo çıkarımı  
3. Kolon adlarının uyumlaştırılması  
4. Kayıt temizliği  
5. NLP normalizasyonu  
6. Fuzzy matching ile eşleştirme  
7. Eksik/ödenmemiş işlemlerin tespiti  
8. Kronolojik sıralama  
9. Excel’e çıktı alma  

---

# 🧪 Demo  
You can test the workflow using the provided sample PDF/Excel invoices and doctor logs.

---

# 📝 License  
This project is for educational and prototyping purposes only. No real patient data is used.

