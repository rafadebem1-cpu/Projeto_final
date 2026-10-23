# API de Reconhecimento de Dígitos Manuscritos com Inteligência Artificial

## 1. Sobre o projeto

Este projeto tem como objetivo desenvolver uma API para reconhecimento de dígitos manuscritos utilizando técnicas de Machine Learning.

O modelo foi treinado com o conjunto de dados MNIST, composto por imagens de dígitos de 0 a 9. Cada imagem é representada por 784 pixels, correspondentes a uma imagem em escala de cinza de 28 × 28 pixels.

O algoritmo escolhido foi o Support Vector Machine (SVM), que apresentou acurácia de aproximadamente 98,3% na avaliação realizada durante o treinamento.

A aplicação foi desenvolvida em Python com FastAPI e permite enviar os pixels de uma imagem para obter a previsão do dígito correspondente.

## 2. Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- Scikit-learn
- NumPy
- Joblib
- Pandas
- Pydantic

## 3. Estrutura do projeto

```text
Projeto_final/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers.py
│   ├── schemas.py
│   └── services.py
├── models/
│   ├── svm_mnist.joblib
│   └── metricas.json
├── notebooks/
├── mini_projeto_final.ipynb
├── requirements.txt
└── README.md
```

## 4. Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/rafadabem1-cpu/Projeto_final.git
cd Projeto_final
```

Crie e ative um ambiente virtual, se ainda não tiver um.

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## 5. Executando a API

Na pasta raiz do projeto, execute:

```bash
python -m uvicorn app.main:app --reload
```

Após a inicialização, a API estará disponível localmente em:

http://127.0.0.1:8000

A documentação interativa pode ser acessada em:

http://127.0.0.1:8000/docs

## 6. Endpoints disponíveis

### GET /health

Verifica se a aplicação está funcionando e se o modelo foi carregado.

Exemplo de resposta:

```json
{
  "status": "ok",
  "modelo_carregado": true
}
```

### POST /predict

Recebe uma lista com exatamente 784 pixels, com valores entre 0 e 255, e retorna o dígito previsto pelo modelo.

Exemplo de requisição:

```json
{
  "pixels": [0, 0, 0, 0]
}
```

**Observação:** o exemplo acima é apenas ilustrativo. Para uma requisição válida, a lista deve conter exatamente 784 valores inteiros entre 0 e 255.

Exemplo de resposta:

```json
{
  "predicted_digit": 1
}
```

O dígito retornado é ilustrativo; a previsão depende dos pixels enviados.

## 7. Validação dos dados

A aplicação utiliza modelos Pydantic para validar a entrada da API.

A validação verifica se:

- A lista contém exatamente 784 pixels.
- Cada pixel está no intervalo de 0 a 255.
- A resposta contém um dígito entre 0 e 9.

Entradas inválidas são rejeitadas pela API com o código HTTP 422.

## 8. Modelo de Machine Learning

O modelo SVM treinado é armazenado no arquivo `models/svm_mnist.joblib`.

O modelo é carregado durante a inicialização da aplicação e reutilizado nas requisições, evitando carregá-lo novamente a cada previsão.

As métricas do treinamento estão registradas em `models/metricas.json`.

A acurácia observada na avaliação foi de aproximadamente 98,3%. Esse resultado se refere à avaliação realizada com o conjunto de teste utilizado no projeto e não garante a mesma precisão para qualquer imagem enviada à API.

## 9. Objetivo educacional

O projeto integra conceitos de análise de dados, Machine Learning, validação de dados, desenvolvimento de APIs e organização modular de aplicações Python.

Foi desenvolvido como parte do projeto final do curso técnico de Análise de Dados e Machine Learning.

## 10. Autor

Projeto acadêmico desenvolvido para fins de estudo e aplicação prática de Inteligência Artificial.