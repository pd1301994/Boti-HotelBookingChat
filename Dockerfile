# Usa la imagen oficial de Python
FROM python:3.10-slim

# Define el directorio de trabajo
WORKDIR /app

# We are copying requirements.txt
COPY requirements.txt .

# Update pip 
RUN python -m pip install --upgrade pip

# installing all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project
COPY . .

# Necessary ports
EXPOSE 5005
EXPOSE 5055
EXPOSE 8000

# Rasa, actions and fast api
CMD ["/bin/bash", "-c", "rasa run --enable-api --cors '*' & rasa run actions & cd frontend && uvicorn main:app --host 0.0.0.0 --port 8000"]
