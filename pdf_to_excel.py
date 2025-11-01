import streamlit as st
import pdfplumber
import pandas as pd

st.title("📄 PDF to Excel Converter (Java-Free)")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
page_input = st.text_input("Enter page number(s) (e.g., 3 or 3,4 or 3-5):")

if uploaded_file and page_input:
    # Parse page input
    try:
        # Handle ranges like "3-5" or lists like "3,4"
        pages = []
        for part in page_input.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start - 1, end))  # pdfplumber is 0-indexed
            else:
                pages.append(int(part.strip()) - 1)
    except ValueError:
        st.error("Invalid page input format.")
        st.stop()

    with pdfplumber.open(uploaded_file) as pdf:
        dfs = []
        for p in pages:
            if p < 0 or p >= len(pdf.pages):
                st.warning(f"Page {p+1} is out of range.")
                continue
            table = pdf.pages[p].extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                df.columns = [str(col).strip() for col in df.columns]  # Normalize headers
                dfs.append(df)

    if dfs:
        try:
            combined_df = pd.concat(dfs, ignore_index=True)
            st.success(f"✅ Extracted {len(combined_df)} rows from pages {page_input}")
            st.dataframe(combined_df)
            st.download_button("📥 Download Excel", combined_df.to_excel(index=False), file_name="converted.xlsx")
        except Exception as e:
            st.error(f"Error combining tables: {e}")
    else:
        st.warning("No tables found on selected pages.")
