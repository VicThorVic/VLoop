from asyncio import tasks
from select import select
import socket
from collections import deque
from threading import Thread
import time
import asyncio

asyncio.new_event_loop()

def make_request():
    print("Make request started!")
    print()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    sock.send(b"GET / HTTP/1.1\r\nHost: 0.0.0.0:8000\r\n\r\n")

    yield sock

    resp = sock.recv(4096)
    print(resp)
    sock.close()
    print("make request finished")

tasks = deque()
stopped = {}
def run_qyery():
    while True:
        time.sleep(5)
        while any([tasks, stopped]):
            print(tasks)
            while not tasks:
                ready_to_read, _, _ =select(stopped, [], [])
                for ready in ready_to_read:
                    tasks.append(stopped.pop(ready))
            while tasks:
                task = tasks.popleft()
                try:
                    sock = next(task)
                    stopped[sock] = task
                except StopIteration:
                    print("QUEUE done")


def run_request_procedure():
    print("start")
    print()
    while True:
        print(f"run_request_procedure len tasks: {len(tasks)}")
        print()
        tasks.append(make_request())
        time.sleep(1.0)
t = Thread(target=run_request_procedure)
t.start()
run_qyery()



    