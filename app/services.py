
"""
2. O que esse módulo precisará fazer?

1. Receber o modelo SVM já carregado.
2. Receber a lista validada de 784 pixels.
3. Transformar a lista no formato esperado pelo scikit-learn, uma matriz com uma linha e 784 colunas.
4. Executar predict().
5. Retornar o dígito previsto."""



import numpy as np


def prever_digito(modelo, pixels: list[int]) -> int:
    """
    Recebe 784 pixels entre 0 e 255,
    normaliza os valores para 0 a 1
    e retorna o dígito previsto pelo modelo SVM.
    """

    # Converte a lista em uma matriz NumPy
    imagem = np.array(pixels, dtype=np.float64).reshape(1, 784)

    # Normaliza os pixels para a mesma escala do treinamento
    imagem = imagem / 255.0

    # Realiza a previsão
    previsao = modelo.predict(imagem)

    # Retorna o dígito como inteiro
    return int(previsao[0])

from io import BytesIO

import numpy as np
from PIL import Image, ImageOps, ImageStat


def converter_imagem_em_pixels(conteudo: bytes) -> list[int]:
    """Converte uma imagem manuscrita em uma lista de 784 pixels."""

    try:
        imagem = Image.open(BytesIO(conteudo)).convert("L")
    except Exception as erro:
        raise ValueError("O arquivo enviado não é uma imagem válida.") from erro

    # Se o fundo for claro, inverte para aproximar o padrão MNIST:
    # fundo preto e dígito branco.
    if ImageStat.Stat(imagem).mean[0] > 127:
        imagem = ImageOps.invert(imagem)

    # Remove ruídos fracos e mantém os traços mais visíveis.
    imagem = imagem.point(lambda pixel: 255 if pixel > 50 else 0)

    # Recorta o conteúdo que representa o dígito.
    caixa = imagem.getbbox()

    if caixa is None:
        raise ValueError("Não foi identificado nenhum dígito na imagem.")

    imagem = imagem.crop(caixa)

    # Redimensiona o dígito preservando sua proporção.
    imagem.thumbnail((20, 20), Image.Resampling.LANCZOS)

    # Cria uma tela preta de 28 x 28 pixels.
    tela = Image.new("L", (28, 28), 0)

    # Centraliza o dígito na tela.
    x = (28 - imagem.width) // 2
    y = (28 - imagem.height) // 2
    tela.paste(imagem, (x, y))

    # Retorna os 784 pixels em escala de cinza.
    return list(tela.getdata())
