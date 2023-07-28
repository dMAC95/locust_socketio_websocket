I found it tricky to implement testing for sockets in locust, but got it working through persistence. With this example resource you should be able to use locust with websockets / socketio relatively easy. You can comment out or delete the websocket / socketio class you don't need. The MyUser class is required for socketio testing in this implementation. This code is very minimal and is supplied as a working base example to build from, it could use more error handling. 

This example was built with locust version 2.15.1
