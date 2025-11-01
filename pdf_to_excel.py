import streamlit as st
import pdfplumber
import pandas as pd

st.title("📄 PDF to Excel Converter (Java-Free)")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
page_input = st.text_input("Enter page number (e.g., 3 or 3,4):")

if uploaded_file and page_input:
    pages = [int(p.strip()) - 1 for p in page_input.replace("-", ",").split(",")]

    with pdfplumber.open(uploaded_file) as pdf:
        dfs = []
        for p in pages:
            page = pdf.pages[p]
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                dfs.append(df)

    if dfs:
        combined_df = pd.concat(dfs)
        st.dataframe(combined_df)
        st.download_button("📥 Download Excel", combined_df.to_excel(index=False), file_name="converted.xlsx")
    else:
        st.warning("No tables found on selected pages.")
