# -*- coding: utf-8 -*-
import os
import json
import time
from kafka import KafkaConsumer

# Configuración vía variables de entorno para flexibilidad en K8s
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC_NAME = 'sensor-data'

def get_consumer():
    try:
        # group_id permite que múltiples consumidores se repartan el trabajo si escalamos
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',  # Si es nuevo, lee desde el principio del historial
            group_id='sensor-group',
            enable_auto_commit=True
        )
        print(f"Consumidor conectado a {KAFKA_BOOTSTRAP_SERVERS}")
        return consumer
    except Exception as e:
        print(f"Esperando a Kafka... Error: {e}")
        return None

if __name__ == "__main__":
    print("Iniciando Consumidor de Datos...")

    consumer = None
    while not consumer:
        consumer = get_consumer()
        if not consumer:
            time.sleep(5)

    try:
        # Bucle principal de lectura bloqueante
        for message in consumer:
            data = message.value
            print(f"Recibido: Sensor {data.get('sensor_id')} | Temp: {data.get('temperature')} | Offset: {message.offset}")
            
    except KeyboardInterrupt:
        print("Cerrando consumidor.")
        if consumer:
            consumer.close()