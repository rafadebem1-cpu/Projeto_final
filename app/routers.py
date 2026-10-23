
""" 
Nesta etapa, o arquivo routers.py vai receber as requisições de previsão e encaminhá-las ao serviço SVM.
"""


from fastapi import APIRouter, HTTPException, Request

from app.schemas import PredictionRequest, PredictionResponse
from app.services import prever_digito


router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(dados: PredictionRequest, request: Request):
    try:
        modelo = request.app.state.modelo
        digito = prever_digito(modelo, dados.pixels)

        return PredictionResponse(predicted_digit=digito)

    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao realizar a previsão."
        ) from erro


"""
>> o que acabou de implementar:
APIRouter(): organiza as rotas da API em um módulo separado.
@router.post("/predict"): cria o endpoint que receberá os pixels por uma requisição HTTP POST.
PredictionRequest: valida os dados de entrada antes da execução da função.
request.app.state.modelo: acessa o modelo que será carregado na inicialização da aplicação.
prever_digito(...): chama o serviço que você já testou.
PredictionResponse: estrutura a resposta com o dígito previsto.
HTTPException: permite devolver um erro HTTP caso ocorra uma falha inesperada na previsão.

"""