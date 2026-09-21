# 🚀 Mecánica Social IA - Runtime Perimetral (MVP)

Mecánica Social IA es el cerebro técnico y motor de automatización asíncrono del ecosistema. Su propósito principal es recibir postulaciones de alumnos en texto libre, procesarlas mediante Inteligencia Artificial, extraer sus campos limpios de forma estructurada y guardarlos con total persistencia relacional bajo estrictos acuerdos contractuales.

---

## 🛡️ Características Principales del Sistema

* **Aduana Contractual (INT-001 e INT-002):** Validaciones perimetrales dobles y cruzadas mediante JSON Schema Draft-07 que mitigan alucinaciones de la IA.
* **Seguridad Perimetral:** Defensa dura contra ráfagas de tráfico mediante un limitador (`PerimetralRateLimiter`) y protección contra caídas de proveedores usando un disyuntor (`IA_CircuitBreaker`).
* **Resiliencia Exponencial:** Cliente de red saliente blindado con algoritmo de Backoff Exponencial y Jitter (ruido aleatorio) para soportar intermitencias.
* **Persistencia Relacional:** Ciclo de vida integrado (Lifespan) que autogestiona e inicializa una base de datos SQLite en el disco duro.
* **Monitoreo Cromático:** Sistema de observabilidad avanzada con marcas de tiempo legibles (`YYYY-MM-DD HH:MM:SS`) y códigos de color ANSI.

---

## 📊 Suite de Calidad de Software
El repositorio cuenta con una batería de **14 pruebas unitarias automatizadas en Pytest (100% Passed)** con cero advertencias, garantizando la inmunidad del Runtime ante regresiones lógicas.

---

## 🧰 Guía Rápida de Comandos Conquistados

Utiliza esta matriz de referencia rápida para gestionar la infraestructura y el ciclo de vida del repositorio desde la terminal:

| Herramienta | Comando Exacto | Propósito Técnico Operacional |
| :--- | :--- | :--- |
| **Git** | `git status` | Audita el estado actual del árbol de trabajo y archivos modificados. |
| **Git** | `git checkout -b <nombre-rama>` | Crea y se desplaza a una nueva rama de desarrollo aislada. |
| **Git** | `git add .` | Empaqueta todos los cambios del disco en la zona de preparación (Staging). |
| **Git** | `git commit -m "<mensaje>"` | Registra un hito formal en el historial bajo estándares de gobernanza. |
| **Git** | `git push --set-upstream origin <rama>` | Sube la rama local a GitHub y establece la ruta de seguimiento. |
| **Git** | `git switch main` | Regresa de forma segura a la rama madre principal del proyecto. |
| **Git** | `git pull origin main` | Descarga y fusiona las últimas actualizaciones unificadas desde la nube. |
| **Docker** | `docker compose up --build` | Compila las imágenes desde cero y enciende los contenedores en vivo. |
| **Docker** | `docker compose up -d` | Levanta la infraestructura en segundo plano (Modo Desacoplado). |
| **Docker** | `docker compose down` | Detiene los servicios y remueve redes privadas de forma limpia. |
| **Docker** | `docker compose up --force-recreate` | Purga las capas de caché antiguas y obliga a reconstruir el entorno. |
| **Pytest** | `python3 -m pytest app/test_api.py -v` | Ejecuta los 14 robots unitarios mostrando el desglose detallado de éxito. |

---

## 🚀 Instrucciones de Arranque Local

1. Enciende los microservicios en segundo plano:
   ```bash
   docker compose up -d --build
   ```
2. Abre la pestaña **Ports** de tu entorno y navega al puerto `8000`.
3. Añade `/docs` a la barra de direcciones del navegador web para interactuar de forma gráfica con la API mediante **Swagger UI**.
4. Autoriza la sección utilizando el token criptográfico: `<API_KEY>`.
