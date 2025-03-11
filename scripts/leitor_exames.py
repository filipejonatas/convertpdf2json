from pdf2image import convert_from_path
import pytesseract
import json
import os

# Caminho para o executável Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Caminho para o executável do Poppler
POPPLER_PATH = r'C:\Poppler_24.0.8\poppler-24.08.0\Library\bin'

# Função para converter PDF em imagens
def pdf_para_imagens(caminho_pdf):
    return convert_from_path(caminho_pdf, poppler_path=POPPLER_PATH)

# Função para extrair texto de uma imagem usando OCR
def extrair_texto_da_imagem(imagem):
    return pytesseract.image_to_string(imagem, lang='por')

# Função para salvar dados em JSON
def salvar_json(dados, caminho_arquivo):
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

# Função principal para processar um PDF
def processar_exame(caminho_pdf, pasta_output):
    # Passo 1: Converter PDF em imagens
    imagens = pdf_para_imagens(caminho_pdf)
    
    texto_extraido = []
    for i, imagem in enumerate(imagens):
        texto = extrair_texto_da_imagem(imagem)
        texto_extraido.append({"pagina": i + 1, "conteudo": texto})
    
    # Passo 2: Salvar os resultados como JSON
    nome_arquivo = os.path.basename(caminho_pdf).replace(".pdf", ".json")
    caminho_json = os.path.join(pasta_output, nome_arquivo)
    salvar_json(texto_extraido, caminho_json)
    print(f"Exame processado e salvo em: {caminho_json}")

# Executar o script
if __name__ == "__main__":
    pasta_input = "input"  # Pasta de entrada
    pasta_output = "output"  # Pasta de saída
    
    # Certifique-se de que as pastas existam
    os.makedirs(pasta_input, exist_ok=True)
    os.makedirs(pasta_output, exist_ok=True)
    
    # Processar todos os PDFs na pasta de entrada
    for arquivo in os.listdir(pasta_input):
        if arquivo.endswith(".pdf"):
            caminho_pdf = os.path.join(pasta_input, arquivo)
            processar_exame(caminho_pdf, pasta_output)
