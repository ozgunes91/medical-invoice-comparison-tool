import pandas as pd

def read_excel_file(uploaded_file):
    """Read a single Excel file and map columns to: patient, date, exam.

    The function is flexible about column names: it normalizes headers to lowercase
    and strips whitespace, then maps common Spanish/English variants.
    """
    df = pd.read_excel(uploaded_file)
    if df.empty:
        raise ValueError(f"Excel file '{uploaded_file.name}' is empty or invalid.")

    # Normalize header names
    df.columns = df.columns.str.lower().str.strip()

    rename_map = {
        # patient
        "nombre del paciente": "patient",
        "nombre paciente": "patient",
        "paciente": "patient",
        "patient": "patient",
        "nombre": "patient",
        "nombre y apellidos": "patient",
        # date
        "fecha": "date",
        "fecha examen": "date",
        "fecha del examen": "date",
        "date": "date",
        # exam
        "descripción del examen": "exam",
        "descripcion del examen": "exam",
        "descripción": "exam",
        "descripcion": "exam",
        "examen": "exam",
        "exam": "exam",
        "nombre examen": "exam",
    }

    df = df.rename(columns={c: rename_map.get(c, c) for c in df.columns})

    required = ["patient", "date", "exam"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns in Excel file '{uploaded_file.name}': {missing}"
        )

    # Only keep the required columns in a stable order
    return df[required].copy()
