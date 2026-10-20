# Practica1AyD

# Práctica CI/CD - SmartCampus

## Descripción
Microservicio REST desarrollado en Flask para la gestión de aulas y reservas en un entorno universitario. El proyecto implementa un flujo completo de Integración y Entrega Continua (CI/CD), asegurando la calidad del código mediante pruebas automatizadas y despliegues estandarizados.

## Tecnologías Utilizadas
* **Backend:** Python (Flask), Pytest, Black
* **Contenedores:** Docker, Docker Compose
* **Control de Calidad Local:** Git Hooks
* **CI/CD:** GitHub Actions

## Ejecución Local con Docker
Para ejecutar el entorno localmente, es necesario configurar las variables de entorno y construir el contenedor.

1. Crear un archivo `.env` en la raíz del proyecto basándose en `.env.example`:
   ```text
   APP_ENV=development
   PORT=5000
