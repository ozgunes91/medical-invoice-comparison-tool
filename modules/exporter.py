from io import BytesIO
import pandas as pd

def export_excel(df: pd.DataFrame) -> BytesIO:
    """Export a DataFrame of unpaid exams to an in-memory Excel file.

    - Renames columns to Spanish as requested by the client:
        patient -> 'Nombre del paciente'
        date    -> 'Fecha (dd/mm/aaaa)'
        exam    -> 'Descripción del examen'
    - Drops helper columns like 'month' and 'day' if present.
    """

    # Work on a copy to avoid side effects
    out_df = df.copy()

    # Drop helper columns not needed in the final Excel
    for col in ["month", "day", "_merge"]:
        if col in out_df.columns:
            out_df = out_df.drop(columns=[col])

    # Rename main columns to Spanish labels
    rename_map = {
        "patient": "Nombre del paciente",
        "date": "Fecha (dd/mm/aaaa)",
        "exam": "Descripción del examen",
    }
    out_df = out_df.rename(columns={c: rename_map.get(c, c) for c in out_df.columns})

    # Ensure column order (only those three are guaranteed)
    ordered_cols = [
        "Nombre del paciente",
        "Fecha (dd/mm/aaaa)",
        "Descripción del examen",
    ]
    existing_cols = [c for c in ordered_cols if c in out_df.columns]
    out_df = out_df[existing_cols]

    output = BytesIO()
    out_df.to_excel(output, index=False)
    output.seek(0)
    return output
