# 🏫 SmartCampus API - Gestión de Aulas y Reservas

![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue)
![Flask](https://img.shields.io/badge/Flask-RESTful-lightgrey)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)

Microservicio REST diseñado para la consulta de aulas y gestión de reservas en recintos universitarios. El proyecto sirve como prueba de concepto para la automatización de infraestructura, implementando control de calidad local mediante Git Hooks y un pipeline de Integración y Entrega Continua (CI/CD) completamente contenerizado.

## 🏗️ Arquitectura y Stack Tecnológico

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
