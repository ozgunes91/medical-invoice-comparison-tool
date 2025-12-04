import pandas as pd
import unicodedata
from rapidfuzz import fuzz, process

def _norm_text(s):
    if pd.isna(s):
        return ""
    s = str(s).strip().lower()
    # Remove accents (e.g., ‘tórax’ → ‘torax’)
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s

def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # required columns
    for col in ["patient", "date", "exam"]:
        if col not in df.columns:
            raise ValueError(f"Beklenen kolon yok: '{col}'")

    # normalize date
    df["date_norm"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce").dt.date

    # normalize text
    df["patient_norm"] = df["patient"].apply(_norm_text)
    df["exam_norm"] = df["exam"].apply(_norm_text)

    # drop empty rows
    df = df.dropna(subset=["patient_norm", "date_norm", "exam_norm"])

    return df


def find_unpaid(doctor_df: pd.DataFrame,
                invoice_df: pd.DataFrame,
                threshold: int = 75) -> pd.DataFrame:
    """
    Returns doctor exams that are NOT present in invoices (unpaid).

    Match rules:
      - same normalized patient
      - same normalized date
      - exam matched by fuzzy token_sort_ratio >= threshold
        with invoice counts respected (1 paid exam can only match 1 doctor exam)
    """

    doc = _prepare(doctor_df)
    inv = _prepare(invoice_df)

    unpaid_records = []

    # group by same patient and date
    grouped_doc = doc.groupby(["patient_norm", "date_norm"], sort=False)

    for (p_norm, d_norm), doc_group in grouped_doc:
        inv_group = inv[(inv["patient_norm"] == p_norm) & (inv["date_norm"] == d_norm)]

        # “if no invoice exists for that day → all exams are unpaid”
        if inv_group.empty:
            unpaid_records.extend(doc_group.to_dict("records"))
            continue

        # treat invoice exam entries as a multiset (counts matter)
        inv_exams = list(inv_group["exam_norm"])

        for _, row in doc_group.iterrows():
            doc_exam = row["exam_norm"]

            if not inv_exams:
                # “no invoice exams remain → all remaining doctor exams are unpaid”
                unpaid_records.append(row.to_dict())
                continue

            # “find the best match using rapidfuzz (score + index)”
            best_score = 0
            best_idx = None

            for idx, paid_exam in enumerate(inv_exams):
                score = fuzz.token_sort_ratio(doc_exam, paid_exam)
                if score > best_score:
                    best_score = score
                    best_idx = idx

            if best_score >= threshold and best_idx is not None:
                # “the invoice record for this exam is now consumed”
                inv_exams.pop(best_idx)
            else:
                unpaid_records.append(row.to_dict())

    if not unpaid_records:
        return pd.DataFrame(columns=["patient", "date", "exam"])

    result = pd.DataFrame(unpaid_records)

    # “return only the original columns”
    result = result[["patient", "date", "exam"]]

    return result
