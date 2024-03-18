# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 20:14:37 2024

@author: ricky
"""

import fitz  # PyMuPDF
import re
import pdfplumber
import pandas as pd
import streamlit as st


# Assuming pdf_path is defined and points to your actual PDF file

def extract_data_from_pdf(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    complete_txt = ""
    
    # Extract the text from each page
    for page in doc:
        complete_txt += page.get_text()
    
    # Define regular expressions
    regex_isin = r"ISIN:\s*([A-Z0-9]+)"  # 
    regex_sri = r"al livello (\d) su 7"
    regex_rhp = r"Periodo di detenzione raccomandato:\s*(\d+) anni"
    regex_nome_prodotto = r"Prodotto:\s*([^[\]()\n-]+)"
    regex_nome_emittente = r"Emittente:\s*([^\n]+)"
    regex_target_market = r"Investitor(?:e|i) al dettaglio .*? investimento:\s*(((?:\d{1,3}(?:\.\d{3})*€\s*)|[^.])*)\."


    
    # Utilize regular expression to find the data
    isin = re.search(regex_isin, complete_txt)
    sri = re.search(regex_sri, complete_txt)
    rhp = re.search(regex_rhp, complete_txt)
    nome_prodotto = re.search(regex_nome_prodotto, complete_txt)
    nome_emittente = re.search(regex_nome_emittente, complete_txt)
    target_market = re.search(regex_target_market, complete_txt)  
    
    
    # Extraction of SCENARI DI PERFORMANCE A RHP
    keywords = ["Stress", "Sfavorevole", "Moderato", "Favorevole"]

    def extract_performance_rhp(pdf_path, keywords):
        all_data = []
        keyword_index = 0  # Initialize a counter to track the current keyword

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_lines = page.extract_text().split('\n')
                for line in text_lines:
                    # Look for lines containing "Rendimento medio annuo"
                    if "Rendimento medio annuo" in line:
                        percentages = re.findall(r'-?\d+[.,]\d+%', line)
                        # Ensure there's a keyword available to pair with the percentages
                        if keyword_index < len(keywords) and percentages:
                            # Append current keyword and percentages to all_data
                            all_data.append([keywords[keyword_index]] + percentages[:])
                            keyword_index += 1  # Move to the next keyword for the next matching line
                    else:
                        # For lines without "Rendimento medio annuo", check if they contain any of the keywords
                        for keyword in keywords:
                            if keyword in line: 
                                # If a keyword is found and there are percentages, associate them with the keyword
                                percentages = re.findall(r'\-?\d+[.,]\d+ %', line) 
                                all_data.append([keyword] + percentages[:])
                                break  # Once a keyword match is found, no need to check the remaining keywords for this line

        # Reset keyword_index if you need to loop through keywords again for additional pages

        return all_data
    
    data = extract_performance_rhp(pdf_path, keywords)



    df = pd.DataFrame(data, columns=['Scenari', '% a 1 anno', '% a RHP'])

    # Find indices of rows that contain 'none' (case insensitive and regardless of leading/trailing spaces)
    indices_to_remove = []
    for index, row in df.iterrows():
        if any('none' in str(cell).lower().strip() for cell in row.values):
            indices_to_remove.append(index)
            
    # Drop the rows with 'none'
    df.drop(indices_to_remove, inplace=True)

    
    doc.close()
    ######### modified version of the output of the function to suite streamlit
    return   {
            "ISIN": isin.group(1) if isin else "Not found",
            "SRI": sri.group(1) if sri else "Not found",
            "RHP": rhp.group(1) if rhp else "Not found",
            "Nome del prodotto": nome_prodotto.group(1) if nome_prodotto else "Not found",
            "Nome dell'emittente": nome_emittente.group(1) if nome_emittente else "Not found",
            "Target Market": target_market.group(1) if target_market else "Not found",
            "Scenari di performance": df[['Scenari', '% a RHP']]
        
        }


#################################################### Streamlit UI
st.title("PDF Data Extractor") 

uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")


if uploaded_file is not None:
    with st.spinner('Extracting data...'):
    
        data_options = ["ISIN", "SRI", "RHP", "Nome del prodotto", "Nome dell'emittente", "Target Market", "Scenari di performance"]
        options = st.multiselect("Select the data you want to extract:", data_options, default=data_options)
        
        
            
    if st.button("Extract Data"):
            with st.spinner('Extracting data...'):  # just to visualize the loading of the data
                extracted_data = extract_data_from_pdf(uploaded_file)  # we extract every key...
                # Check and display each selected option appropriately
                st.subheader("Extracted Data")
                for key in options:   # .. but we print only the keys appearing in options
                    if key == "Scenari di performance":
                        st.markdown(f"**{key}:**")
                        st.dataframe(extracted_data[key])
                    else:
                        value = extracted_data.get(key, "Not found")
                        st.markdown(f"**{key}:** {value}")
