# Usa la imagen oficial de Python
FROM python:3.10

# Define el directorio de trabajo
WORKDIR /app

# Copia solo el archivo requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .

# Actualiza pip a la última versión
RUN python -m pip install --upgrade pip

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto después de instalar las dependencias
COPY . .

# Expone los puertos necesarios
EXPOSE 5005
EXPOSE 5055
EXPOSE 8000

# Comando para ejecutar Rasa, las acciones y FastAPI
CMD ["/bin/bash", "-c", "rasa run --enable-api --cors '*' & rasa run actions & cd frontend && uvicorn main:app --host 0.0.0.0 --port 8000"]
