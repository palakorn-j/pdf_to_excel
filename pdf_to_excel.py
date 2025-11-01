import streamlit as st
import pdfplumber
import pandas as pd
import io

st.set_page_config(page_title="PDF to Excel Converter", layout="centered")
st.title("📄 PDF to Excel Converter (Java-Free)")
st.markdown("Upload a PDF and specify which pages to extract tables from.")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

# Page input
page_input = st.text_input("Enter page numbers (e.g., 3, 3-4, or 3,4):")

# Helper to deduplicate column names
def dedup_columns(cols):
    seen = {}
    new_cols = []
    for col in cols:
        col = str(col).strip()
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}.{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    return new_cols

# Convert button
if uploaded_file and page_input:
    try:
        # Parse page input
        pages = []
        for part in page_input.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start - 1, end))  # pdfplumber uses 0-based indexing
            else:
                pages.append(int(part.strip()) - 1)

        # Extract tables
        dfs = []
        with pdfplumber.open(uploaded_file) as pdf:
            for p in pages:
                if p < 0 or p >= len(pdf.pages):
                    st.warning(f"Page {p+1} is out of range.")
                    continue
                table = pdf.pages[p].extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=dedup_columns(table[0]))
                    dfs.append(df)

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            st.success(f"✅ Extracted {len(combined_df)} rows from pages {page_input}")
            st.dataframe(combined_df)

            # Prepare Excel for download
            output = io.BytesIO()
