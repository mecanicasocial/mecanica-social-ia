import time
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IA-Client")

class IAClient:
    def __init__(self, max_retries=3, base_delay=1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def generar_respuesta(self, prompt: str) -> str:
        """
        Ejecuta la llamada al modelo con estrategia de reintentos y Exponential Backoff.
        """
        delay = self.base_delay

        for intento in range(1, self.max_retries + 1):
            try:
                return self._invocar_llm(prompt)
            except Exception as error:
                logger.warning(f"Intento {intento}/{self.max_retries} falló: {error}")
                if intento == self.max_retries:
                    logger.error("Se agotaron los reintentos permitidos.")
                    raise error

                tiempo_espera = delay * (2 ** (intento - 1)) + random.uniform(0, 0.1)
                logger.info(f"Reintentando en {tiempo_espera:.2f} segundos...")
                time.sleep(tiempo_espera)

    def _invocar_llm(self, prompt: str) -> str:
        if not prompt:
            raise ValueError("El prompt no puede estar vacío.")
        return f"Respuesta generada para: '{prompt[:30]}...'"
