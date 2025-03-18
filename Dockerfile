# Use a imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY requirements.txt requirements.txt
COPY app.py app.py

# Instala as dependências
RUN pip install -r requirements.txt

# Exponha a porta 8501 (padrão do Streamlit)
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
