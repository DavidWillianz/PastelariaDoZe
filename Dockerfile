# Usa uma imagem base enxuta com Python 3.13
FROM python:3.13-slim

# Metadados da imagem
LABEL maintainer="David Willian <davidcosta@uniplaclages.edu.br>"
LABEL description="API Python com FastAPI, Hypercorn e QUIC"
LABEL version="1.0.0"

# Define o diretório de trabalho
WORKDIR /code

# Copia o requirements.txt e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia o código-fonte e define o novo diretório de trabalho
COPY scr/ /code/scr
WORKDIR /code/scr

# Copia os certificados para o container
COPY cert/ /cert

# Copia o banco de dados SQLite (caso necessário para execução local)
COPY comandas_db.db /code/comandas_db.db

# Expõe a porta TCP e UDP 4443
EXPOSE 4443/tcp
EXPOSE 4443/udp

# Comando para iniciar o servidor Hypercorn com suporte a HTTP3/QUIC
CMD ["hypercorn", \
    "--certfile=/cert/cert.pem", "--keyfile=/cert/ecc-key.pem", \
    "--bind", "0.0.0.0:4443", "--quic-bind", "0.0.0.0:4443", \
    "main:app"]


# 1. Construir a imagem com nome comanda-api (sem necessidade do -f se o nome for Dockerfile)
# docker build -t comanda-api .

# # 2. Criar uma tag para enviar ao Docker Hub
# docker tag comanda-api davidwillianz/comanda-api

# # 3. Enviar a imagem para seu repositório no Docker Hub
# docker push davidwillianz/comanda-api
