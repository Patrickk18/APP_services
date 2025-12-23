# APP_services

 # 🚀 APP_services: Arquitectura Híbrida de Microservicios en Kubernetes

 ![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
 ![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
 ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 ![Apache NiFi](https://img.shields.io/badge/Apache%20NiFi-729FCF?style=for-the-badge&logo=apache&logoColor=white)

 Este repositorio contiene la implementación de una **Arquitectura Orientada a Eventos (EDA)** y de Procesamiento de Datos Híbrido. El sistema integra microservicios desarrollados en Python, un bus de mensajería Apache Kafka y orquestación de datos con Apache NiFi, todo desplegado sobre un clúster local de **Kubernetes**.

 ---

 ## 🏗️ Arquitectura del Sistema

 El proyecto se despliega bajo el namespace `paradigma` y consta de los siguientes componentes:

 * **Producer Service (Python):** Genera datos de telemetría simulada (sensores de temperatura/humedad) y los publica en el tópico `sensor-data`.
 * **Consumer Service (Python):** Se suscribe al tópico `sensor-data`, procesa los mensajes en tiempo real y registra la actividad en consola.
 * **Apache Kafka & Zookeeper:** Middleware de mensajería que desacopla los servicios, garantizando la transmisión asíncrona y resiliente.
 * **Apache NiFi:** Herramienta ETL desplegada en el clúster para la orquestación visual, ingesta y transformación de flujos de datos.

 ---

 ## 📂 Estructura del Proyecto

 ```text
 APP_services/
 ├── k8s/                  # Manifiestos de Kubernetes (Infraestructura como Código)
 │   ├── apps/             # Deployments del Producer y Consumer
 │   ├── kafka/            # Configuración de Kafka (Broker) y Zookeeper
 │   └── nifi/             # Despliegue de Apache NiFi y Servicios
 ├── src/                  # Código fuente de los Microservicios
 │   ├── producer-service/ # Script Python + Dockerfile del Productor
 │   └── consumer-service/ # Script Python + Dockerfile del Consumidor
 ├── nifi-templates/       # Plantillas XML de respaldo para flujos de NiFi
 └── docs/                 # Documentación y evidencias del proyecto
 ```

 ---

 ## ⚙️ Pre-requisitos

 * **Docker Desktop** instalado y corriendo.
 * **Kubernetes** habilitado en Docker Desktop (*Settings -> Kubernetes -> Enable*).
 * Consola de comandos (PowerShell, Bash o CMD).

 ---

 ## 🚀 Instalación y Despliegue

 Sigue estos pasos para levantar toda la infraestructura desde cero.

 ### 1. Clonar el repositorio
 ```bash
 git clone <URL_DEL_REPOSITORIO>
 cd APP_services/APP_services
 ```

 ### 2. Construir las imágenes Docker
 Empaquetamos el código Python en contenedores locales para que Kubernetes pueda usarlos.
 ```bash
 docker build -t producer:latest ./src/producer-service/
 docker build -t consumer:latest ./src/consumer-service/
 ```

 ### 3. Desplegar en Kubernetes
 Aplicamos todos los manifiestos de forma recursiva. Esto crea el namespace `paradigma`, los servicios (`kafka-svc`, `zookeeper`, `nifi`) y los deployments.
 ```bash
 kubectl apply -R -f k8s/
 ```

 ### 4. Verificar el estado
 Espera unos minutos a que descarguen las imágenes y verifica que todos los pods estén en estado `Running`.
 ```bash
 kubectl get pods -n paradigma
 ```

 ---

 ## 🧪 Pruebas y Validación

 ### 📡 1. Verificar Comunicación (Microservicios)
 Para confirmar que los datos fluyen a través de Kafka en tiempo real, revisa los logs del consumidor. Deberías ver la llegada de datos JSON de los sensores.
 ```bash
 kubectl logs -n paradigma -l app=consumer --tail=20 -f
 ```

 ### 🌪️ 2. Acceder a Apache NiFi
 NiFi corre dentro del clúster. Para acceder a su interfaz web, crea un túnel (port-forwarding):
 ```bash
 kubectl port-forward -n paradigma svc/nifi 8080:8080
 ```
 * **URL:** Abre tu navegador en `http://localhost:8080/nifi`
 * **Uso:** Puedes cargar las plantillas desde la carpeta `nifi-templates/` para restaurar flujos visuales.

 ### 📈 3. Prueba de Escalabilidad
 Kubernetes permite escalar horizontalmente los consumidores para manejar más carga. Ejecuta el siguiente comando para triplicar las instancias:
 ```bash
 kubectl scale deployment consumer -n paradigma --replicas=3
 ```
 Verifica que se hayan creado las nuevas instancias distribuyendo la carga:
 ```bash
 kubectl get pods -n paradigma
 ```

 ---

 ## 🛠️ Tecnologías y Versiones
 * **Kubernetes:** v1.25+ (Local Cluster)
 * **Kafka:** Imagen `wurstmeister/kafka:2.13-2.8.1`
 * **Zookeeper:** Imagen oficial `3.5`
 * **Python:** 3.9-slim
 * **Orquestador:** Apache NiFi latest
 * **Librería Kafka:** `kafka-python`

 ---
#
# ## 📝 Autor
# Desarrollado como parte del proyecto de **Arquitectura de Servicios**.
