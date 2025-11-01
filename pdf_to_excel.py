import streamlit as st
import pandas as pd
from tabula import read_pdf
import tempfile
import os

st.title("📄 PDF to Excel Converter (Page-Specific)")
st.markdown("Upload a PDF and specify which pages to extract tables from.")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

# Page input
page_input = st.text_input("Enter page numbers (e.g., 3, 3-4, or 3,4):")

# Convert button
if uploaded_file and page_input:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    try:
        # Extract tables
        dfs = read_pdf(
            tmp_path,
            pages=page_input,
            multiple_tables=True,
            guess=False,
            lattice=True  # Use stream=True if needed
        )

        # Filter out duplicates
        unique_tables = []
        for df in dfs:
            if not any(df.equals(existing) for existing in unique_tables):
                unique_tables.append(df)

        # Combine and export
        combined_df = pd.concat(unique_tables)
        st.success(f"✅ Extracted {len(combined_df)} rows from pages {page_input}")

        # Show preview
        st.dataframe(combined_df)

        # Download link
        output_path = os.path.join(tempfile.gettempdir(), "converted.xlsx")
        combined_df.to_excel(output_path, index=False)
        with open(output_path, "rb") as f:
            st.download_button("📥 Download Excel File", f, file_name="converted.xlsx")

    except Exception as e:
        st.error(f"❌ Error: {e}")
