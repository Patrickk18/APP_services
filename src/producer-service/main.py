# -*- coding: utf-8 -*-
import time
import json
import random
import os
from kafka import KafkaProducer

# Configuración: Leemos la dirección de Kafka de las variables de entorno (útil para K8s)
# Si no existe, usa localhost por defecto.
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC_NAME = 'sensor-data'

def get_producer():
    try:
        # Instanciamos el productor
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8') # Convertir a JSON automáticamente
        )
        print(f"Conectado exitosamente a Kafka en {KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        print(f"Error conectando a Kafka: {e}")
        return None

def generate_sensor_data():
    # Simula datos de un sensor IoT
    return {
        'sensor_id': random.choice(['S1', 'S2', 'S3']),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 50.0), 2),
        'timestamp': time.time()
    }

if __name__ == "__main__":
    print("Iniciando Productor de Sensores...")
    
    # Intentar conectar (esperar un poco si Kafka no está listo)
    producer = None
    while not producer:
        producer = get_producer()
        if not producer:
            time.sleep(5)

    try:
        while True:
            data = generate_sensor_data()
            # Enviar al tópico
            producer.send(TOPIC_NAME, value=data)
            print(f"Enviado: {data}")
            
            # Esperar 2 segundos entre mensajes
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("Productor detenido.")
        if producer:
            producer.close()