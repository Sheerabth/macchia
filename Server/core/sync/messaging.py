import json
import pika
from .sempahore import CustomSemaphore
from .sync_data import SyncData
from config import Config


def get_semaphore(requested_id):
    if requested_id not in SyncData.semaphore_dict:
        SyncData.semaphore_dict[requested_id] = CustomSemaphore(0)
        query(requested_id)

    return SyncData.semaphore_dict[requested_id]


def query(requested_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='query', exchange_type='fanout')
    print("Querying requested id")
    channel.basic_publish(exchange='query', routing_key='', body=requested_id)
    connection.close()


def query_handler(ch, method, properties, body):
    body = body.decode()
    if Config.NODE_ID == body:
        response_dict = {
            "id": Config.NODE_ID,
            "ip_address": Config.SERVER_IP + ":" + str(Config.SERVER_PORT)
        }

        print("Query handled")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange='response', exchange_type='fanout')
        print("Sending responses")
        channel.basic_publish(exchange='response', routing_key='', body=json.dumps(response_dict))
        connection.close()

    else:
        print("Query not handled")


def response_handler(ch, method, properties, body):
    body = body.decode()
    response_dict = json.loads(body)
    if response_dict["id"] != Config.NODE_ID and response_dict["id"] not in SyncData.cache:
        # time.sleep(10)
        SyncData.cache[response_dict["id"]] = response_dict["ip_address"]
        print("Response updated")
        print("Updated cache:", SyncData.cache)
        if response_dict["id"] in SyncData.semaphore_dict:
            SyncData.semaphore_dict[response_dict["id"]].release_all()


def listen_to_queries():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='query', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='query', queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=query_handler, auto_ack=True)
    print("Listening to queries")
    channel.start_consuming()


def listen_to_responses():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='response', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='response', queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=response_handler, auto_ack=True)
    print("Listening to responses")
    channel.start_consuming()


def get_host(requested_id: str):
    if requested_id == Config.NODE_ID:
        return f"{Config.SERVER_IP}:{Config.SERVER_PORT}"

    if requested_id not in SyncData.cache:
        semaphore = get_semaphore(requested_id)
        semaphore.acquire()

    return SyncData.cache[requested_id]
