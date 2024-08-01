import json
from infraestructure.db import SessionLocal
from domain.models.cloth import Cloth
from application.schemas.base_response import BaseResponse
from http import HTTPStatus
import threading

import pika

def actualizar_status_ropa(ropa_id):
    session = SessionLocal()
    cloth = session.query(Cloth).filter(Cloth.id == ropa_id).first()
    if cloth:
        cloth.status_id = 3
        session.commit()
        session.close()
        return BaseResponse(None, "Status updated successfully", True, HTTPStatus.OK)
    else:
        session.close()
        return BaseResponse(None, "Cloth not found", False, HTTPStatus.NOT_FOUND)

def on_request(ch, method, properties, body):
    message = json.loads(body)
    cloth_id = message.get('cloth_id')

    response = {"error": "Cloth not found"}
    session = SessionLocal()
    cloth = session.query(Cloth).filter(Cloth.id == cloth_id).first()
    if cloth:
        response = {
            "id": cloth.id,
            "uuid": cloth.uuid,
            "type": cloth.type,
            "image": cloth.image,
            "buy": cloth.buy,
            "price": cloth.price,
            "sellPrice": cloth.sellPrice,
            "location": cloth.location,
            "description": cloth.description,
            "size": cloth.size,
            "status_id": cloth.status_id,
            "period_id": cloth.period_id,
            "created_at": cloth.created_at.isoformat(),  # Format date as ISO string
            "sold_at": cloth.sold_at.isoformat() if cloth.sold_at else None  # Format date as ISO string, handle null
        }
    session.close()
    
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_message(ch, method, properties, body):
    print("Message received: ", body)
    message = json.loads(body)
    ropa_id = message.get('ropa_id')
    
    if ropa_id is not None:
        response = actualizar_status_ropa(ropa_id)
        print(response.message)
    else:
        print("Invalid message format")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
def start_consuming_queue(queue_name, callback):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='35.168.45.250', port=5672, virtual_host='/', credentials=pika.PlainCredentials('diego', 'Diegoespro01'))
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    
    print(f"Waiting for messages in {queue_name}. To exit press CTRL+C")
    channel.start_consuming()

def start_consuming():
    queues = [
        ('status_update_queue', on_message),
        ('cloth_request_queue', on_request),
        # Agregar más colas si es necesario
    ]
    
    threads = []
    for queue_name, callback in queues:
        thread = threading.Thread(target=start_consuming_queue, args=(queue_name, callback))
        thread.start()
        threads.append(thread)
    
    # Esperar a que todos los hilos terminen (esto puede ser adaptado según necesidades)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    start_consuming()
