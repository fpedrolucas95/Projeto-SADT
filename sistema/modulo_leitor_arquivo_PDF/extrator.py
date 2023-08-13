from PIL import Image
import pytesseract
from spellchecker.spellchecker import SpellChecker
import numpy as np
from skimage.filters import threshold_sauvola
import json

def preprocessar_imagem(imagem):
    imagem_gray = imagem.convert('L')
    imagem_array = np.array(imagem_gray)
    t_sauvola = threshold_sauvola(imagem_array, window_size=25)
    imagem_binarizada = imagem_array > t_sauvola
    imagem_final = Image.fromarray((imagem_binarizada * 255).astype(np.uint8))
    return imagem_final

def corrigir_texto(texto):
    spell = SpellChecker(language='pt')
    palavras_corrigidas = [spell.correction(palavra) if spell.correction(palavra) is not None else palavra for palavra in texto.split()]
    return ' '.join(palavras_corrigidas)

def extrair_dados_raw(image_path):
    imagem = Image.open(image_path)
    imagem_preprocessada = preprocessar_imagem(imagem)
    texto = pytesseract.image_to_string(imagem_preprocessada, lang='por')
    texto_corrigido = corrigir_texto(texto)

    with open('dados_por_pagina.json', 'a', encoding='utf8') as json_file:
        json.dump([texto_corrigido], json_file, ensure_ascii=False)

    print(texto_corrigido)
    return texto_corrigido
