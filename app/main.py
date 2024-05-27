import socket
from typing import Tuple
import threading
# def handle_client(connection: socket.socket, address: Tuple[str, int]) -> None:
#     with connection:
#         print(f"Accecpted connection from {address}\n")
#         while True:
#             data: bytes = connection.recv(1024)
#             if not data:
#                 break
#             if data:
#                 pong: str = "+PONG\r\n"
#                 connection.sendall(pong.encode())
def handle_connection(conn, addr):
    while True:
        request: bytes = conn.recv(1024)
        if not request:
            break
        data: str = request.decode()
        if "ping" in data.lower():
            response = "+PONG\r\n"
            print(response)
            conn.send(response.encode())
    conn.close()
def main():
    print("Logs from your program will appear here!\n")
    # server_socket: socket.socket = socket.create_server(
    #     ("localhost", 6379), reuse_port=True
    # )
    # while True:
    #     try:
    #         connection: socket.socket
    #         address: Tuple[str, int]
    #         connection, address = server_socket.accept()
    #         # handle_client(connection, address)
    #         client_thread = threading.Thread(
    #             target=handle_client, args=[connection, address]
    #         )
    #         client_thread.start()
    #     except Exception as e:
    #         print(f"Exception: {e}")
    server_socket = socket.create_server(("localhost", 6379))
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Received a connection from {client_address}")
        threading.Thread(
            target=handle_connection, args=[client_socket, client_address]
        ).start()
        # handle_connection(client_socket, client_address)


if __name__ == "__main__":
    main()
