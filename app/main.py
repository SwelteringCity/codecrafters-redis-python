import socket
import os
from threading import *
class Database:
    def __init__(self):
        self.data = {}
    def add(self, key, value):
        self.data[key] = value
    def get(self, key):
        if key not in self.data:
            return -1
        return self.data[key]
class Connection(Thread):
    def __init__(self, socket, address):
        super().__init__()
        self.socket = socket
        self.address = address
        self.database = Database()
        self.start()
    def run(self):
        while True:
            request = self.socket.recv(1024)
            if not request:
                break
            parsedReq = self.parseReq(request)
            self.parseCommandAndSendRequest(parsedReq)
        self.close()
    def parseReq(self, request):
        requestParams = request.decode().split("\r\n")
        return requestParams
    def parseCommandAndSendRequest(self, request):
        requestCommand = request[2].lower()
        if "ping" == requestCommand:
            dataToSend = "+PONG\r\n"
        elif "echo" == requestCommand:
            dataToSend = f"+{request[-2]}\r\n"
        elif "set" == requestCommand:
            self.database.add(request[4], request[6])
            dataToSend = "+OK\r\n"
        elif "get" == requestCommand:
            value = self.database.get(request[-2])
            dataToSend = f"+{value}\r\n"
        else:
            return
        self.socket.send(dataToSend.encode())
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    serverSocket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        # Wait for client
        clientSocket, clientAddress = serverSocket.accept()
        print("Received a connection from client: {clientAddress}")
        Connection(clientSocket, clientAddress)
if __name__ == "__main__":
    main()