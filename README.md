# SmartCampus API - Gestión de Aulas y Reservas

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)
![Flask](https://img.shields.io/badge/Flask-RESTful-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)

Microservicio REST diseñado para la consulta de aulas y gestión de reservas en recintos universitarios. El proyecto sirve como prueba de concepto para la automatización de infraestructura, implementando control de calidad local mediante Git Hooks y un pipeline de Integración y Entrega Continua (CI/CD) completamente contenerizado.

## Arquitectura y Stack Tecnológico

- **Framework:** Python con Flask (memoria volátil para persistencia temporal).
- **Testing:** Pytest (con fixtures en `conftest.py` para aislamiento de estado).
- **Linting & Formato:** Black.
- **Despliegue:** Docker y Docker Compose.
- **Automatización CI/CD:** GitHub Actions (Matriz multi-entorno).

## 📂 Estructura del Proyecto

```text
smartcampus/
├── .git/hooks/           # Scripts de validación local (pre-commit, post-commit, pre-push)
├── .github/workflows/    # Definición del pipeline CI/CD (ci-cd.yml)
├── app/                  # Lógica de negocio y endpoints de Flask
├── tests/                # Suite de pruebas unitarias y de integración
├── Dockerfile            # Receta de construcción de la imagen
├── docker-compose.yml    # Orquestación local de contenedores
└── requirements.txt      # Dependencias estandarizadas
```

## Documentación de la API (Endpoints Principales)

El servicio expone respuestas en formato JSON.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET`  | `/health`| Verifica el estado de ejecución del contenedor. |
| `GET`  | `/rooms` | Devuelve el catálogo completo de aulas disponibles. |
| `POST` | `/bookings`| Registra una nueva reserva (valida solapamientos lógicos). |

## 🚀 Guía de Despliegue Local

1. **Clonar y configurar el entorno:**
   ```bash
   git clone https://github.com/TU_USUARIO/Practica1AyD.git
   cd smartcampus
   cp .env.example .env
   ```

2. **Levantar la infraestructura con Docker:**
   ```bash
   docker compose up --build -d
   ```

3. **Ejecutar la suite de pruebas localmente:**
   ```bash
   python -m pytest -v
   ```

## ⚙️ Flujo de CI/CD (GitHub Actions)

El ciclo de vida del código está fuertemente tipado mediante un pipeline de dos fases que se dispara con cada `push` a la rama `main`:

1. **Fase de Integración (Test & Quality):** 
   Ejecución de trabajos paralelos aislados en Ubuntu. Despliega la aplicación en Python 3.11 y 3.12, verifica el tipado y formato con `Black`, y ejecuta las pruebas de `Pytest`. El fallo de un solo entorno bloquea el pipeline.

2. **Fase de Despliegue (Build & Deploy):** 
   Tras superar la fase de integración, el runner construye la imagen `smartcampus:latest`, instancia un contenedor efímero para realizar un *healthcheck* real mediante cURL, y valida la inyección de secretos del repositorio (`DB_PASSWORD`) para un despliegue simulado seguro.

---

## Mejoras Propuestas para Entorno de Producción

Aunque el proyecto cumple con los requisitos de integración continua, para evolucionar hacia un entorno de grado de producción (Enterprise) se proponen las siguientes mejoras arquitectónicas:

1. **Seguridad DevSecOps (Trivy):** 
   Integrar un escáner de vulnerabilidades en el pipeline para analizar la imagen base de Docker (`python:3.11-slim`) antes de autorizar el despliegue.
2. **Análisis Estático Avanzado (Ruff + MyPy):** 
   Sustituir o complementar `Black` con herramientas que validen el tipado estricto y detecten *code smells* o imports circulares, evitando fallos lógicos en tiempo de compilación.
3. **Orquestación en Clúster (Kubernetes/Minikube):** 
   Sustituir el despliegue efímero de Docker Compose por manifiestos YAML (Deployment, Service, Ingress) para permitir auto-escalado y alta disponibilidad en un clúster de Kubernetes.
4. **Auto-Documentación Viva (Swagger/OpenAPI):** 
   Integrar librerías como `flasgger` para autogenerar una interfaz gráfica en `/apidocs`, permitiendo testear los endpoints directamente desde el navegador sin depender de herramientas externas como Postman.
