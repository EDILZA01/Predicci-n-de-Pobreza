# =============================================================================
# Dockerfile - ENAHO Poverty Prediction Microservice & MLOps Platform
# =============================================================================
# FASE 6: Contenerización de producción ligera y segura basada en Python 3.11-slim

FROM python:3.11-slim

# Variables de entorno para ejecución en contenedores Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalación de paquetes y dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia de manifiesto de dependencias e instalación optimizada en caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia de módulos y artefactos necesarios exclusivamente para producción
COPY api/ ./api/
COPY models/ ./models/
COPY src/ ./src/
COPY data/ ./data/
COPY app.py .

# Exposición del puerto del microservicio REST
EXPOSE 8000

# Comando por defecto para inicializar la API FastAPI con Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
