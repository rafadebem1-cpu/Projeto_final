

from contextlib import asynccontextmanager
from pathlib import Path

import joblib
from fastapi import FastAPI

from app.routers import router


# Caminho do modelo, relativo à estrutura do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "svm_mnist.joblib"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executado uma vez na inicialização da aplicação
    app.state.modelo = joblib.load(MODEL_PATH)

    yield

    # Executado quando a aplicação é encerrada
    del app.state.modelo


app = FastAPI(
    title="API de Reconhecimento de Dígitos",
    description="API para prever dígitos manuscritos usando um modelo SVM.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "modelo_carregado": hasattr(app.state, "modelo"),
    }


app.include_router(router)

"""
>>> Entenda os pontos principais
- Path(__file__).resolve(): encontra o caminho do próprio arquivo, evitando depender da pasta em que o terminal foi aberto.
- joblib.load(MODEL_PATH): carrega o modelo treinado.
- lifespan: executa a inicialização antes de atender às requisições e a rotina de encerramento ao desligar a API.
- app.state.modelo: mantém o modelo disponível para o roteador e o serviço.
- GET /health: permite verificar se a aplicação está funcionando e se o modelo foi carregado.
- app.include_router(router): registra o endpoint POST /predict criado anteriormente.
O uso de lifespan atende ao requisito de arquitetura do projeto: o arquivo de modelo não precisa ser lido a cada previsão.

"""
