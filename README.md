
# API de Reconhecimento de Dígitos Manuscritos com Inteligência Artificial

## 1. Sobre o projeto

Este projeto tem como objetivo desenvolver uma API para reconhecimento de dígitos manuscritos utilizando técnicas de Machine Learning.

O modelo foi treinado com o conjunto de dados **MNIST**, composto por imagens de dígitos de 0 a 9. Cada imagem possui dimensões de 28 × 28 pixels, totalizando 784 pixels em escala de cinza.

O algoritmo escolhido foi o **Support Vector Machine (SVM)**, que apresentou acurácia de aproximadamente **98,3%** na avaliação realizada durante o projeto.

A aplicação foi desenvolvida em Python com FastAPI e permite enviar os pixels de uma imagem para obter a previsão do dígito correspondente.

Além do treinamento do modelo, o projeto contempla a serialização do modelo, a validação dos dados de entrada, o desenvolvimento de uma API modular e a disponibilização de endpoints para consulta e previsão.

## 2. Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- Scikit-learn
- NumPy
- Joblib
- Pandas
- Pydantic
- Pillow — para processamento de imagens, caso utilizado pelo script de teste

As versões das principais dependências estão especificadas no arquivo `requirements.txt`.

## 3. Estrutura do projeto

```text

Projeto_final/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers.py
│   ├── schemas.py
│   └── services.py
├── imagens_teste/
├── models/
│   ├── svm_mnist.joblib
│   └── metricas.json
├── notebooks/
├── mini_projeto_final.ipynb
├── testar_imagem.py
├── requirements.txt
└── README.md

```

### Responsabilidade dos arquivos

- `main.py`: configura a aplicação FastAPI, carrega o modelo na inicialização e disponibiliza o endpoint de saúde.
- `routers.py`: define as rotas da API, incluindo a rota de previsão.
- `schemas.py`: define os esquemas de entrada e saída e as regras de validação dos dados.
- `services.py`: realiza o pré-processamento dos pixels e executa a previsão com o modelo.
- `models/svm_mnist.joblib`: contém o modelo SVM treinado e serializado.
- `models/metricas.json`: armazena as métricas registradas durante a avaliação do modelo.
- `mini_projeto_final.ipynb`: contém o notebook de desenvolvimento e experimentação do projeto.
- `requirements.txt`: lista as dependências necessárias para executar a aplicação.

## 4. Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone https://github.com/rafadebem1-cpu/Projeto_final.git
cd Projeto_final
```

Crie e ative um ambiente virtual.

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

A interface Swagger permite consultar os endpoints e realizar requisições de teste diretamente pelo navegador.

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

Recebe uma lista com exatamente 784 pixels, com valores inteiros entre 0 e 255, e retorna o dígito previsto pelo modelo.

Exemplo de requisição válida, utilizando uma imagem totalmente preta:

```json
{
  "pixels": [0, 0, 0, 0, 0, 0, 0, 0]
}
```

**Importante:** o trecho acima é apenas ilustrativo e não constitui uma requisição válida. Para realizar uma previsão, a lista deve conter exatamente 784 valores inteiros entre 0 e 255.

Para realizar uma requisição válida, envie exatamente 784 valores inteiros entre 0 e 255. Você pode gerar uma requisição de teste pelo Swagger, disponível em /docs.

Exemplo de resposta:

```json
{
  "predicted_digit": 1
}
```

O resultado acima é ilustrativo. A previsão real depende dos pixels enviados.

## 7. Reconhecimento de imagens manuscritas

Além do endpoint que recebe uma lista de pixels, a API permite enviar imagens diretamente pelo endpoint `POST /predict/image`.

O endpoint aceita imagens PNG e JPEG. Arquivos inválidos ou imagens sem um dígito identificável são rejeitados.

O arquivo enviado é processado pela aplicação, convertido para escala de cinza, ajustado para o formato 28 × 28 pixels e transformado em uma lista de 784 valores. Em seguida, os pixels são normalizados e enviados ao modelo SVM para a previsão.

**Códigos de resposta HTTP**

- `200 OK`: imagem processada e dígito previsto com sucesso.
- `400 Bad Request`: arquivo vazio, imagem inválida ou nenhum dígito identificado.
- `415 Unsupported Media Type`: arquivo enviado em formato diferente de PNG ou JPEG.
- `503 Service Unavailable`: modelo de previsão indisponível.
- `500 Internal Server Error`: erro inesperado durante a previsão.


### Como testar

1. Inicie a API.
2. Acesse `http://127.0.0.1:8000/docs`.
3. Localize `POST /predict/image`.
4. Clique em **Try it out** e selecione uma imagem PNG.
5. Clique em **Execute** e confira o dígito previsto.

As imagens de teste ficam armazenadas na pasta `imagens_teste/`. O desempenho depende da qualidade da imagem, da legibilidade do dígito e da semelhança entre a escrita enviada e as imagens utilizadas no treinamento.

O endpoint aceita imagens PNG e JPEG. Arquivos inválidos ou imagens sem um dígito identificável são rejeitados.

## 8. Validação dos dados

A aplicação utiliza Pydantic para validar os dados recebidos pela API.

A validação verifica se:

- A lista contém exatamente 784 pixels.
- Cada pixel é um número inteiro.
- Cada pixel está no intervalo de 0 a 255.
- Não existem campos adicionais não permitidos na requisição.
- O dígito retornado pelo modelo está entre 0 e 9.
- A requisição não pode conter campos adicionais além dos definidos no esquema.
- Valores decimais, textos ou outros tipos que não sejam inteiros são rejeitados para os pixels.


Requisições que não atendem aos critérios de validação são rejeitadas com o código HTTP `422`.

Se o modelo não estiver disponível, a API pode retornar HTTP `503`. Erros inesperados durante a previsão são tratados pela aplicação com HTTP `500`.

## 9. Modelo de Machine Learning

O modelo escolhido foi o Support Vector Machine (SVM), treinado com o conjunto de dados MNIST.

O arquivo serializado está localizado em:

`models/svm_mnist.joblib`

O modelo é carregado durante a inicialização da aplicação e armazenado no estado da aplicação FastAPI. Dessa forma, ele pode ser reutilizado nas requisições, sem precisar ser carregado novamente a cada previsão.

Antes de realizar a previsão, os valores dos pixels são normalizados para o intervalo de 0 a 1, conforme o pré-processamento utilizado no treinamento.

As métricas registradas durante a avaliação estão disponíveis em:

`models/metricas.json`

Na avaliação realizada com o conjunto de teste do MNIST, o modelo SVM apresentou os seguintes resultados:

- **Acurácia:** 98,30%
- **Precisão ponderada (Weighted Precision):** 98,30%
- **Revocação ponderada (Weighted Recall):** 98,30%
- **F1-score ponderado (Weighted F1-score):** 98,30%

Essas métricas representam o desempenho do modelo na avaliação realizada com o conjunto de teste. O resultado não garante o mesmo desempenho para qualquer imagem manuscrita enviada à API, pois a qualidade da escrita e o processamento da imagem podem influenciar a previsão.

## 10. Objetivo educacional

O projeto integra conceitos de análise de dados, Machine Learning, avaliação de modelos, serialização, validação de dados, desenvolvimento de APIs e organização modular de aplicações Python.

Foi desenvolvido como parte do projeto final do curso técnico de Análise de Dados e Machine Learning.

## 11. Autor

Projeto acadêmico desenvolvido para fins de estudo e aplicação prática de Inteligência Artificial.

## 12. Apresentação do projeto

**Vídeo de demonstração:** *link a ser inserido após a publicação.*

A apresentação demonstrará o objetivo do projeto, a execução da aplicação, os testes dos endpoints da API, o funcionamento do modelo SVM e as principais decisões técnicas adotadas durante o desenvolvimento.

O vídeo será disponibilizado por meio de um link acessível para avaliação.