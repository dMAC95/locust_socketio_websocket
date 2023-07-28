import time
import websocket
import socketio
from locust import User, task, between, events

# class SocketIoUser(User):
#     wait_time = between(0.1, 0.5)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client = socketio.Client()
#         self.client.on('test', self.on_message)  # Define an event handler for 'message' event
#         self.connection_status = False
#         try:
#             self.client.connect('http://127.0.0.1:8000')
#             self.connection_status = True
#             events.request.fire(request_type="ws connect", name="ws",  response_time=0, response_length=0)
#         except Exception as e:
#             events.request.fire(request_type="ws connect", name="ws", exception=e, response_time=0, response_length=0)

#     @task
#     def my_task(self):
#         if self.connection_status:
#             self.start_time = time.time()
#             self.client.emit('test', {"data": "test"})  # Emit a 'message' event with some data

#     def on_message(self, data):
#         """Event handler for 'message' event"""
#         total_time = int((time.time() - self.start_time) * 1000)  # response time in milliseconds
#         events.request.fire(request_type="ws recv", name="ws", response_time=total_time, response_length=len(str(data)))

#     def on_stop(self):
#         self.client.disconnect()

# class MyUser(SocketIoUser):
#     pass

class WebSocketUser(User):
    wait_time = between(1, 2)

    def on_start(self):
        self.connection_status = False
        try:
            self.client = websocket.create_connection("ws://127.0.0.1:8000/test")
            self.connection_status = True
            events.request.fire(request_type="ws connect", name="ws",  response_time=0, response_length=0)
        except Exception as e:
            print(e)
            events.request.fire(request_type="ws connect", name="ws", exception=e, response_time=0, response_length=0)
        

    def on_stop(self):
        if self.connection_status:
            self.client.close()

    @task
    def ws_task(self):
        if self.connection_status:
            request = '{"message":"test"}'
            start_time = time.time()
            self.client.send(request)
            response = self.client.recv()
            total_time = int((time.time() - start_time) * 1000)  # response time in milliseconds
            events.request.fire(request_type="ws", name="", response_time=total_time, response_length=0)