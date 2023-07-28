import time
import websocket
import socketio
from locust import User, task, between, events

class SocketIoUser(User):
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = socketio.Client()
        self.client.on('test', self.on_message)  # Define an event handler for 'message' event
        self.client.connect('locahost')

    @task
    def my_task(self):
        self.start_time = time.time()
        self.client.emit('test', {"data": "test"})  # Emit a 'message' event with some data

    def on_message(self, data):
        """Event handler for 'message' event"""
        total_time = int((time.time() - self.start_time) * 1000)  # response time in milliseconds
        events.request.fire(request_type="ws recv", name="ws", response_time=total_time, response_length=len(str(data)))

    def on_stop(self):
        self.client.disconnect()

class MyUser(SocketIoUser):
    pass

class WebSocketUser(User):
    wait_time = between(1, 2)

    def on_start(self):
        self.client = websocket.create_connection("ws://localhost")

    def on_stop(self):
        self.client.close()

    @task
    def ws_task(self):
        request = '{"message":"test"}'
        start_time = time.time()
        self.client.send(request)
        response = self.client.recv()
        total_time = int((time.time() - start_time) * 1000)  # response time in milliseconds
        events.request.fire(request_type="ws", name="", response_time=total_time, response_length=0)