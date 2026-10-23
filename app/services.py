
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
    Recebe 784 pixels e retorna o dígito previsto pelo modelo SVM.
    """

    # Transforma a lista em uma matriz com 1 linha e 784 colunas
    imagem = np.array(pixels).reshape(1, 784)

    # Executa a previsão usando o modelo já carregado
    previsao = modelo.predict(imagem)

    # Retorna o resultado como um número inteiro
    return int(previsao[0])
