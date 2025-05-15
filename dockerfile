# Imagem base
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Evita que Python gere arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que a saída do Python seja enviada imediatamente para o terminal
ENV PYTHONUNBUFFERED=1

# Instala as dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o código do projeto
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
