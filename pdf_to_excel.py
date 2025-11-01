import streamlit as st
import tabula
import pandas as pd
import io

st.set_page_config(page_title="PDF to Excel Converter")
st.title("📄 PDF to Excel Converter (tabula-py + Java)")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
page_input = st.text_input("Enter page numbers (e.g., 1, 2-3):")

if uploaded_file and page_input:
    try:
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        # Parse page input
        pages = []
        for part in page_input.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start, end + 1))
            else:
                pages.append(int(part.strip()))

        # Extract tables
        dfs = tabula.read_pdf("temp.pdf", pages=pages, multiple_tables=True, lattice=True)

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            st.dataframe(combined_df)

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
