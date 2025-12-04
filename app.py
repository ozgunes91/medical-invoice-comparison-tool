import streamlit as st
import pandas as pd

from modules.pdf_reader import read_pdf_invoices
from modules.excel_reader import read_excel_file
from modules.normalizer import normalize_df
from modules.matcher import find_unpaid
from modules.exporter import export_excel

st.set_page_config(page_title="Medical Invoice Comparison Tool", layout="wide")

# ---------------------------------------------------------
#                 FULL PREMIUM MEDICAL SAAS UI
# ---------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ------------ COLOR SYSTEM (Enterprise Medical Palette) ------------ */
:root {
    --primary: #1E4D8B;
    --primary-light: #3C7DC0;
    --navy: #1C2A45;
    --grey-dark: #4D596A;
    --grey-light: #E4E8EF;
    --bg: #F7FAFD;
    --card-bg: #FFFFFF;
    --border: #DCE3EB;
    --success-bg: #CFEED1;
}

/* ------------ BASE LAYOUT ------------ */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.main {
    padding: 0px 40px 40px 40px !important;
    background-color: var(--bg);
}

/* ------------ HEADER (Apple/Stripe style) ------------ */
header {
    background-color: white !important;
    border-bottom: 1px solid rgba(28,42,69,0.07);
    backdrop-filter: blur(6px);
}

/* ------------ TITLES ------------ */
h1 {
    font-weight: 750 !important;
    font-size: 2.35rem !important;
    color: var(--navy) !important;
    letter-spacing: -0.32px !important;
}
h2, h3 {
    font-weight: 650 !important;
    color: var(--navy) !important;
}

/* ------------ MICRO DESCRIPTION (UNDER MAIN TITLE) ------------ */
.page-subtitle {
    font-size: 0.98rem;
    color: #6B7484;
    margin-top: 0.15rem;
    margin-bottom: 1.6rem;
    letter-spacing: -0.1px;
}

/* ------------ SECTION CARD ------------ */
.section-card {
    background: var(--card-bg);
    padding: 28px;
    border-radius: 16px !important;
    border: 1px solid var(--border);
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    margin-bottom: 32px;
}

/* ------------ PREMIUM DIVIDER ------------ */
hr.premium-divider {
    border: 0;
    border-top: 1px solid rgba(210, 222, 236, 0.95);
    margin: 0.5rem 0 1.6rem 0;
}

/* ------------ FILE UPLOADER + ICON FLOAT ------------ */
.stFileUploader > div {
    background: #EEF3F8;
    padding: 15px;
    border-radius: 12px !important;
    border: 1px dashed #B5C7DA;
}
.stFileUploader:hover > div {
    border: 1px dashed var(--primary-light);
    background: #E8F2FD;
}
.stFileUploader svg {
    color: var(--primary-light) !important;
    opacity: 0.9;
    animation: uploaderFloat 2.6s ease-in-out infinite;
}
@keyframes uploaderFloat {
    0%   { transform: translateY(0px);    opacity: 0.85; }
    50%  { transform: translateY(-3px);   opacity: 1.00; }
    100% { transform: translateY(0px);    opacity: 0.85; }
}

/* ------------ COMPARE BUTTON (PRIMARY) ------------ */
div.stButton {
    display: flex !important;
    align-items: center !important;
}
div.stButton > button {
    background: linear-gradient(135deg, #1E4D8B, #2F6EB3) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 12px 28px !important;
    border-radius: 10px !important;
    border: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 48px !important;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.12) !important;
    letter-spacing: -0.2px !important;
}
/* Hover */
div.stButton > button:hover {
    background: linear-gradient(135deg, #163C70, #265A96) !important;
    transform: translateY(-1px) !important;
}

/* Click animation (loading pulse effect) */
@keyframes comparePulse {
    0%   { box-shadow: 0px 3px 8px rgba(0,0,0,0.18); }
    50%  { box-shadow: 0px 6px 16px rgba(0,0,0,0.30); }
    100% { box-shadow: 0px 3px 8px rgba(0,0,0,0.18); }
}
div.stButton > button:active {
    animation: comparePulse 0.45s ease-out;
}

/* ------------ SECONDARY DOWNLOAD BUTTON ------------ */
.stDownloadButton > button {
    padding: 0.75rem 1.4rem !important;
    background: #F1F4F8 !important;
    color: #1E4D8B !important;
    border: 1px solid #D6DFEA !important;
    border-radius: 10px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
.stDownloadButton > button:hover {
    background: #E7ECF3 !important;
}

/* ------------ TABLE (Soft shadow + round edges) ------------ */
[data-testid="stDataFrame"] {
    background: var(--card-bg);
    padding: 20px;
    border-radius: 16px !important;
    border: 1px solid var(--grey-light);
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.03);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
#                      PAGE TITLE
# ---------------------------------------------------------
st.title("Medical Invoice Comparison Tool")
st.markdown(
    "<p class='page-subtitle'>AI-assisted reconciliation of clinic invoices with "
    "doctor’s real work logs, highlighting unpaid exams for finance and audit teams in seconds.</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
#                        UPLOAD SECTION
# ---------------------------------------------------------
st.subheader("1. Upload Files")
st.markdown(
    "<hr class='premium-divider'/>",
    unsafe_allow_html=True
)

pdf_files = st.file_uploader("Upload PDF invoices (one or more)", type=["pdf"], accept_multiple_files=True)
excel_invoices = st.file_uploader("Upload Excel invoices (optional)", type=["xlsx"], accept_multiple_files=True)
worklogs = st.file_uploader("Upload Doctor Work Logs (required)", type=["xlsx"], accept_multiple_files=True)

# ---------------------------------------------------------
#                      COMPARE BUTTON
# ---------------------------------------------------------
if st.button("Compare"):
    with st.spinner("Processing..."):

        df_paid = pd.DataFrame()
        df_logs = pd.DataFrame()

        # Load PDFs
        for f in pdf_files or []:
            df_pdf = read_pdf_invoices(f)
            df_paid = pd.concat([df_paid, df_pdf], ignore_index=True)

        # Load Excel invoices
        for f in excel_invoices or []:
            df_x = read_excel_file(f)
            df_paid = pd.concat([df_paid, df_x], ignore_index=True)

        # Load doctor logs
        for f in worklogs or []:
            df_l = read_excel_file(f)
            df_logs = pd.concat([df_logs, df_l], ignore_index=True)

        df_paid = normalize_df(df_paid)
        df_logs = normalize_df(df_logs)

        unpaid = find_unpaid(df_logs, df_paid)
        # ---------------------------
        # SORT RESULTS (correct chronological order → then patient)
        # ---------------------------
        if not unpaid.empty:
            unpaid["date_dt"] = pd.to_datetime(unpaid["date"], dayfirst=True)
            unpaid = unpaid.sort_values(["date_dt", "patient"], ignore_index=True)
            unpaid = unpaid.drop(columns=["date_dt"])

    # ---------------------------------------------------------
    #                   RESULT SECTION
    # ---------------------------------------------------------
    st.subheader("2. Unpaid Exams Result")
    st.dataframe(unpaid, use_container_width=True)

    # Export
    file_bytes = export_excel(unpaid)
    st.download_button(
        label="Download Unpaid Exams Excel",
        data=file_bytes,
        file_name="unpaid_exams.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


