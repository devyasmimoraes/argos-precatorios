from fpdf import FPDF
import sys
import json

def criar_pdf(dados_json):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Relatório de Precatórios - GPX Investimentos", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=10)
    # Cabeçalho da Tabela
    pdf.cell(80, 10, "Processo", border=1)
    pdf.cell(60, 10, "Status", border=1, ln=True)
    
    for item in dados_json:
        # Trata caracteres especiais para não dar erro no PDF
        processo = str(item.get('Processo', '-'))
        status = str(item.get('status', '-'))
        
        pdf.cell(80, 10, processo, border=1)
        pdf.cell(60, 10, status, border=1, ln=True)
    
    pdf.output("/app/relatorio_final.pdf")

if __name__ == "__main__":
    try:
        input_data = sys.stdin.read()
        dados = json.loads(input_data)
        criar_pdf(dados)
        print("PDF gerado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")