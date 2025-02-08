#!/bin/bash

# Iniciar Kafka
/etc/confluent/docker/run &

# Esperar a que Kafka esté listo
echo "Esperando a que Kafka esté listo..."
sleep 10

# Crear el topic
echo "Creando el topic 'users_created'..."
kafka-topics --bootstrap-server broker:29092 --create --topic users_created --partitions 1 --replication-factor 1

# Mantener el contenedor en ejecución
wait