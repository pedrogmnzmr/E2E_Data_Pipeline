import uuid
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

# Configuración predeterminada del DAG
default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 9, 3, 10, 00)
}

# Función para obtener datos de la API
def get_data():
    import requests
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]
    return res

# Función para formatear los datos
def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())  # Convertir UUID a string para compatibilidad con bases de datos
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data

# Función para insertar datos en la base de datos
def insert_data_to_db(data):
    from cassandra.cluster import Cluster
    try:
        # Conectar al clúster de Cassandra
        cluster = Cluster(['cassandra'])  # Cambia esto si tu Cassandra no está en localhost
        session = cluster.connect('users_keyspace')  # Reemplaza 'users_keyspace' con tu keyspace

        # Insertar datos en la tabla
        query = """
        INSERT INTO users (id, first_name, last_name, gender, address, post_code, email, username, dob, registered_date, phone, picture)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        session.execute(query, (
            data['id'],
            data['first_name'],
            data['last_name'],
            data['gender'],
            data['address'],
            data['post_code'],
            data['email'],
            data['username'],
            data['dob'],
            data['registered_date'],
            data['phone'],
            data['picture']
        ))
        logging.info(f"Datos insertados correctamente: {data['id']}")
    except Exception as e:
        logging.error(f"Error al insertar datos en la base de datos: {e}")
    finally:
        cluster.shutdown()

# Función principal para transmitir datos
def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60:  # Duración de 1 minuto
            break
        try:
            res = get_data()
            formatted_data = format_data(res)

            # Enviar datos a Kafka
            producer.send('users_created', json.dumps(formatted_data).encode('utf-8'))

            # Insertar datos en la base de datos
            insert_data_to_db(formatted_data)

        except Exception as e:
            logging.error(f'An error occurred: {e}')
            continue

# Definición del DAG
with DAG('user_automation',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )

    # Si necesitas dividir las tareas, puedes crear otra tarea específica para insertar en la base de datos