import pdfplumber
import pandas as pd
from io import BytesIO
import re
from .normalizer import normalize_text

def read_pdf_invoices(pdf_files):

    # Accept single file or list
    if not isinstance(pdf_files, (list, tuple)):
        pdf_files = [pdf_files]

    all_rows = []

    for uploaded_file in pdf_files:

        # Convert to file-like
        if isinstance(uploaded_file, (bytes, bytearray)):
            file_obj = BytesIO(uploaded_file)
            source_name = "uploaded_bytes.pdf"
        else:
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
            file_obj = uploaded_file
            source_name = getattr(uploaded_file, "name", "unknown.pdf")

        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if not table:
                    continue

                raw_header = table[0]
                raw_rows = table[1:]

                if not raw_rows:
                    continue

                # Normalize headers
                header = [str(h).lower().strip() for h in raw_header]

                rename_map = {
                    "nombre del paciente": "patient",
                    "paciente": "patient",
                    "patient": "patient",
                    "nombre paciente": "patient",
                    "fecha": "date",
                    "date": "date",
                    "fecha examen": "date",
                    "procedimiento": "exam",
                    "examen": "exam",
                    "exam": "exam",
                    "descripcion": "exam",
                    "descripción": "exam"
                }

                mapped_header = [rename_map.get(h, h) for h in header]

                # Convert rows
                fixed_rows = []
                last_patient = None
                last_date = None

                for row in raw_rows:
                    # Pad row
                    if len(row) < len(mapped_header):
                        row = list(row) + [None] * (len(mapped_header) - len(row))
                    row_dict = dict(zip(mapped_header, row))

                    # Normalize text fields
                    for key in ["patient", "date", "exam"]:
                        if key in row_dict and row_dict[key]:
                            row_dict[key] = normalize_text(str(row_dict[key]))
                        else:
                            row_dict[key] = None

                    # Fill missing patient/date from previous row
                    if row_dict["patient"] is None and last_patient:
                        row_dict["patient"] = last_patient
                    if row_dict["date"] is None and last_date:
                        row_dict["date"] = last_date

                    # If exam is split into next row, skip invalid ones
                    if row_dict["exam"] is None:
                        continue

                    last_patient = row_dict["patient"]
                    last_date = row_dict["date"]

                    # Store row
                    row_dict["_source"] = source_name
                    row_dict["_page"] = page.page_number
                    fixed_rows.append(row_dict)

                all_rows.extend(fixed_rows)

    if not all_rows:
        return pd.DataFrame(columns=["patient", "date", "exam"])

    df = pd.DataFrame(all_rows)

    # Clean final DataFrame
    df = df.dropna(subset=["patient", "date", "exam"])

    # Fix date formats
    def fix_date(x):
        x = x.replace("-", "/")
        if re.match(r"\d{1,2}/\d{1,2}/\d{4}", x):
            return x
        if re.match(r"\d{1,2}/\d{1,2}/\d{2}", x):
            d,m,y = x.split("/")
            return f"{d}/{m}/20{y}"
        return x

    df["date"] = df["date"].apply(fix_date)

    return df[["patient", "date", "exam"]]
