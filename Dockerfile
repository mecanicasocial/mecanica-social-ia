# ==============================================================================
# INFRAESTRUCTURA DE CONTENEDORES - MECÁNICA SOCIAL IA (CONTRATO INT-001)
# ==============================================================================
FROM python:3.14-slim

# Evita que Python escriba archivos .pyc en el disco del contenedor
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que los logs de FastAPI se impriman de inmediato en la consola del orquestador
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema mínimas requeridas si fuesen necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el manifiesto de requisitos e instalar las librerías oficiales del Runtime
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la estructura del servidor y los componentes nativos de Inteligencia Artificial
COPY app/ ./app/
COPY src/ms_ia/ ./ms_ia/
COPY data/ ./data/
COPY prompts/ ./prompts/

# Seguridad Perimetral: Crear un usuario no-root para aislar el proceso de ejecución
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto de escucha configurado para el contrato REST
EXPOSE 8000

# Comando de arranque por defecto levantando el servidor Uvicorn de alta concurrencia
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
