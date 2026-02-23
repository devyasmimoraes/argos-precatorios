import pdfplumber
import pandas as pd
import re
import os

pdf_path = "Y26.pdf"
dados_extraidos = []

print(f"Iniciando a mineração do arquivo {pdf_path}...")

if not os.path.exists(pdf_path):
    print(f"Erro: O arquivo {pdf_path} não foi encontrado na pasta.")
    exit()

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            linhas = text.split('\n')
            for linha in linhas:
                # Pega os 20 números do processo
                match_processo = re.search(r'\b\d{20}\b', linha)
                if match_processo:
                    processo = match_processo.group(0)
                    match_data = re.search(r'\d{2}/\d{2}/\d{4}', linha)
                    data = match_data.group(0) if match_data else "Sem Data"
                    match_valor = re.search(r'\d{1,3}(?:\.\d{3})*,\d{2}', linha)
                    valor = match_valor.group(0) if match_valor else "0,00"
                    
                    dados_extraidos.append({"Processo": processo, "Data": data, "Valor": valor})
        
        if (i + 1) % 50 == 0:
            print(f"Páginas processadas: {i + 1}...")

df = pd.DataFrame(dados_extraidos)
nome_csv = "lista_precatorios.csv"
df.to_csv(nome_csv, index=False, encoding='utf-8')

print("\n--- RESUMO DA EXTRAÇÃO ---")
print(f"Processos encontrados: {len(df)}")
print(f"Arquivo gerado: {nome_csv} 🚀")