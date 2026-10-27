
""" 
Nesta etapa, o arquivo routers.py vai receber as requisições de previsão e encaminhá-las ao serviço SVM.
"""
from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    UploadFile,
    File,
)
from app.services import (
    prever_digito,
    converter_imagem_em_pixels,
)

from app.schemas import PredictionRequest, PredictionResponse

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(dados: PredictionRequest, request: Request):
    """
    Recebe os pixels de uma imagem e retorna o dígito previsto.
    """

    # Verifica se o modelo está disponível
    modelo = getattr(request.app.state, "modelo", None)

    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo de previsão indisponível."
        )

    try:
        # Executa a previsão por meio do serviço
        digito = prever_digito(modelo, dados.pixels)

        # Retorna a previsão validada pelo schema de resposta
        return PredictionResponse(predicted_digit=digito)

    except HTTPException:
        raise

    except Exception as erro:
        # Registra o erro no terminal para facilitar o diagnóstico
        print(f"Erro durante a previsão: {erro}")

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao realizar a previsão."
        ) from erro

@router.post("/predict/image")
async def predict_image(
    request: Request,
    arquivo: UploadFile = File(...),
):
    """Recebe uma imagem e retorna o dígito previsto."""

    if arquivo.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(
            status_code=415,
            detail="Envie uma imagem PNG ou JPEG.",
        )

    conteudo = await arquivo.read()

    if not conteudo:
        raise HTTPException(
            status_code=400,
            detail="O arquivo enviado está vazio.",
        )

    try:
        pixels = converter_imagem_em_pixels(conteudo)
    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro),
        ) from erro

    modelo = getattr(request.app.state, "modelo", None)

    if modelo is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo de previsão indisponível.",
        )

    try:
        digito = prever_digito(modelo, pixels)
        return {"predicted_digit": digito}
    except Exception as erro:
        print(f"Erro durante a previsão da imagem: {erro}")
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao realizar a previsão.",
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