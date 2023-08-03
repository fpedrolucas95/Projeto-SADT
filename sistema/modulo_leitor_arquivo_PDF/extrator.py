from PIL import Image
import pytesseract
import spacy
import json

nlp = spacy.load('pt_core_news_lg')

def extrair_dados_raw(image_path):
    imagem = Image.open(image_path)
    dados_por_pagina = []

    for i in range(imagem.n_frames):
        imagem.seek(i)
        texto = pytesseract.image_to_string(imagem, lang='por')
        dados_relevantes = extrair_dados_relevantes(texto)
        dados_por_pagina.append(dados_relevantes)
        
    with open('dados_por_pagina.json', 'w', encoding='utf8') as json_file:
        json.dump(dados_por_pagina, json_file, ensure_ascii=False)

    print(dados_por_pagina)
    return dados_por_pagina

def extrair_dados_relevantes(texto):
    doc = nlp(texto)
    entidades_nomeadas = [(entidade.text, entidade.label_) for entidade in doc.ents]
    return entidades_nomeadas
