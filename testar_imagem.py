

from PIL import Image, ImageOps
from pathlib import Path
import json
import urllib.request

# Caminho da imagem
caminho = Path("imagens_teste") / "imagem_9.png"

# Abre a imagem em escala de cinza
imagem = Image.open(caminho).convert("L")

# Inverte as cores: fundo preto e traço branco
imagem = ImageOps.invert(imagem)

# Separa o desenho do fundo usando um limiar
imagem = imagem.point(lambda pixel: 255 if pixel > 100 else 0)

# Recorta a área que contém o dígito
caixa = imagem.getbbox()

if caixa is None:
    raise ValueError("Nenhum desenho foi encontrado na imagem.")

imagem = imagem.crop(caixa)

# Redimensiona o dígito para caber em uma área de 20 x 20
imagem.thumbnail((20, 20), Image.Resampling.LANCZOS)

# Centraliza em uma imagem de 28 x 28, como no MNIST
tela = Image.new("L", (28, 28), 0)
posicao = (
    (28 - imagem.width) // 2,
    (28 - imagem.height) // 2
)
tela.paste(imagem, posicao)

# Converte os 784 pixels para uma lista de 0 a 255
pixels = list(tela.get_flattened_data())

# Monta a requisição para a API
dados = json.dumps({"pixels": pixels}).encode("utf-8")

requisicao = urllib.request.Request(
    "http://127.0.0.1:8000/predict",
    data=dados,
    headers={"Content-Type": "application/json"},
    method="POST"
)

# Envia a imagem para a API
with urllib.request.urlopen(requisicao) as resposta:
    resultado = json.loads(resposta.read().decode("utf-8"))

print("Dígito esperado: 9")
print("Previsão do modelo:", resultado["predicted_digit"])

# Salva a imagem processada para inspeção
tela.save("imagens_teste/digito_processado.png")
print("Imagem processada salva em imagens_teste/digito_processado.png")
