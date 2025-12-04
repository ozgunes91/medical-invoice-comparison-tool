import pandas as pd
import unicodedata
from dateutil.parser import parse
import re

def normalize_text(value):
    """Lowercase, strip, remove accents, collapse spaces, strip punctuation-like noise."""
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()

    # Normalize accents
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove most punctuation (keep alphanumerics and spaces)
    text = re.sub(r"[^\w\s]", "", text)

    return text.strip()

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize patient/exam text fields and dates to dd/mm/yyyy strings."""

    df = df.copy()

    # Normalize patient and exam names
    if "patient" in df.columns:
        df["patient"] = df["patient"].apply(normalize_text)
    if "exam" in df.columns:
        df["exam"] = df["exam"].apply(normalize_text)

    # Date normalization
    if "date" in df.columns:
        def parse_date_safe(x):
            if pd.isna(x) or x == "":
                return None
            try:
                # dayfirst=True → dd/mm/yyyy gibi formatlar için
                return parse(str(x), dayfirst=True)
            except Exception:
                return None

        parsed = df["date"].apply(parse_date_safe)
        df["date"] = pd.to_datetime(parsed, errors="coerce")

        # Final formatting to dd/mm/yyyy (string); unmatched will be NaT → NaN
        df["date"] = df["date"].dt.strftime("%d/%m/%Y")

    return df
