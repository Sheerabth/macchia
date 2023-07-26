import json
import pika
import sys
from threading import Thread, Lock, Semaphore
from fastapi import FastAPI, Request
import uvicorn
import time

semaphores_dict = dict()


class DECSemaphore:
    def __init__(self, value: int) -> None:
        self.semaphore = Semaphore(value)
        self.waiting = 0
        self.count_lock = Lock()

    def acquire(self):
        self.count_lock.acquire()
        self.waiting += 1
        self.count_lock.release()
        self.semaphore.acquire()

    def release(self):
        self.semaphore.release()
        self.count_lock.acquire()
        self.waiting -= 1
        self.count_lock.release()

    def release_all(self):
        print(f"Releasing {self.waiting} threads")
        if self.waiting != 0:
            self.semaphore.release(self.waiting)
        self.count_lock.acquire()
        self.waiting = 0
        self.count_lock.release()


def get_semaphore(requested_id):
    global semaphores_dict
    if requested_id not in semaphores_dict:
        semaphores_dict[requested_id] = DECSemaphore(0)
        query(requested_id)

    return semaphores_dict[requested_id]


def query(requested_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='query', exchange_type='fanout')
    print("Querying requested id")
    channel.basic_publish(exchange='query', routing_key='', body=requested_id)
    connection.close()


def query_handler(ch, method, properties, body):
    global node_id
    global ip_address
    body = body.decode()
    if node_id == body:
        response_dict = {
            "id": node_id,
            "ip_address": ip_address
        }
        print("Query handled")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='response', exchange_type='fanout')
        print("Sending responses")
        channel.basic_publish(exchange='response', routing_key='', body=json.dumps(response_dict))
        connection.close()

    else:
        print("Query not handled")


def response_handler(ch, method, properties, body):
    global cache
    global semaphores_dict
    body = body.decode()
    response_dict = json.loads(body)
    if response_dict["id"] != node_id and response_dict["id"] not in cache:
        time.sleep(10)
        cache[response_dict["id"]] = response_dict["ip_address"]
        print("Response updated")
        print("Updated cache:", cache)
        if response_dict["id"] in semaphores_dict:
            semaphores_dict[response_dict["id"]].release_all()


def listen_to_queries():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='query', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='query', queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=query_handler, auto_ack=True)
    print("Listening to queries")
    channel.start_consuming()


def listen_to_responses():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='response', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='response', queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=response_handler, auto_ack=True)
    print("Listening to responses")
    channel.start_consuming()


app = FastAPI()


@app.get('/request_test/something/{path_id}')
def req_test(req: Request, path_id: str):
    print(path_id)
    print(req.url.path)
    print(req.url.scheme)
    print(req.url.query)
    print(req.url.components)


@app.get("/get_cache")
def get_cache():
    return cache


@app.post("/get_ip")
def get_ip(requested_id: str):
    global node_id
    global ip_address
    global cache

    if requested_id == node_id:
        return {"ip_address": ip_address}

    if requested_id not in cache:
        semaphore = get_semaphore(requested_id)
        semaphore.acquire()

    return {"ip_address": cache[requested_id]}


if __name__ == "__main__":
    global node_id
    global ip_address
    global cache
    node_id = sys.argv[1]
    ip_address = sys.argv[2]
    cache = json.loads(sys.argv[3])

    query_thread = Thread(target=listen_to_queries)
    query_thread.start()
    response_thread = Thread(target=listen_to_responses)
    response_thread.start()

    uvicorn.run(app, host="localhost", port=int(ip_address))
