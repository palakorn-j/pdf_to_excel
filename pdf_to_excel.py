import streamlit as st
import tabula
import pandas as pd
import tempfile
import io

st.set_page_config(page_title="PDF to Excel Converter")
st.title("📄 PDF to Excel Converter (tabula-py + Java)")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
page_input = st.text_input("Enter page numbers (e.g., 1, 2-3):")

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
        if dfs:
            combined_df = pd.concat(unique_tables)
            st.success(f"✅ Extracted {len(combined_df)} rows from pages {page_input}")

            # Prepare Excel download
            output = io.BytesIO()
            combined_df.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="📥 Download Excel",
                data=output,
                file_name="converted.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("No tables found.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
