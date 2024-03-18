import fitz  # PyMuPDF
import re
import pdfplumber
import pandas as pd

# Assuming pdf_path is defined and points to your actual PDF file


def extract_data_from_pdf(pdf_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    complete_txt = ""
    
    # Extract the text from each page
    for page in doc:
        complete_txt += page.get_text()
    
    # Define regular expressions
    regex_isin = r"ISIN:\s*([A-Z0-9]+)"
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
    target_market = re.search(regex_target_market, complete_txt)  # re.DOTALL per includere il cambio di linea
    
    
    # Extarction of SCENARI DI PERFORMANCE A RHP
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

        

        return all_data
    
    data = extract_performance_rhp(pdf_path, keywords)



    df = pd.DataFrame(data, columns=['Scenari', '% a 1 anno', '% a RHP'])

    # Find indices of rows that contain 'none' 
    indices_to_remove = []
    for index, row in df.iterrows():
        if any('none' in str(cell).lower().strip() for cell in row.values):
            indices_to_remove.append(index)
            
    # Drop the rows with 'none'
    df.drop(indices_to_remove, inplace=True)

    
    

    # print the results of the extraction
    print("ISIN:", isin.group(1) if isin else "Not found") # .group(1) first group to be extracted
    print("\nSRI:", sri.group(1) if sri else "Not found")
    print("\nRHP:", rhp.group(1) if rhp else "Not found") 
    print("\nNome del prodotto:", nome_prodotto.group(1) if nome_prodotto else "Not found")
    print("\nNome dell'emittente:", nome_emittente.group(1) if nome_emittente else "Not found")
    print("\nTarget market:", target_market.group(1) if target_market else "Not found")
    print("\nScenari di performance:\n\n", df[['Scenari', '% a RHP']])
    print ("\n\n")
    # Close the document
    doc.close()

# path of the pdf file to analyze
file_paths = [r"C:\Users\ricky\Desktop\Prometeia\KID1.pdf",
              r"C:\Users\ricky\Desktop\Prometeia\KID2.pdf",
              r"C:\Users\ricky\Desktop\Prometeia\KID3.pdf",
              r"C:\Users\ricky\Desktop\Prometeia\KID4.pdf"
              ]


for i, file_path in enumerate(file_paths, start=1):
    print(f"KID{i}\n")  # Print "KID1", "KID2", "KID3", "KID4" before processing each file
    extract_data_from_pdf(file_path)


   


