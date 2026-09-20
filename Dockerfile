FROM python:3.14-slim

WORKDIR /app

# Instalación de dependencias del sistema de forma segura
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Creación del usuario de seguridad perimetral no privilegiado
RUN useradd -m -u 8888 appuser
USER appuser

# Configuración del PATH global seguro para el usuario
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copia e instalación de dependencias en el espacio del usuario
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copia de los módulos y capas del Runtime del MVP
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser data/ ./data/
COPY --chown=appuser:appuser prompts/ ./prompts/

EXPOSE 8000

# ENFOQUE INMUNE DE CONFIGURACIÓN DE RED: Llamada directa al módulo nativo de Python
CMD ["python3", "-m", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
