import socket
from threading import Thread
REDIS_PONG = "+PONG\r\n"
DEBUG = False
DELIM = "\r\n"
REDIS_PONG = "+PONG" + DELIM
REDIS_COMMANDS = [
    # REDIS_PONG
    "COMMAND",
    "PING",
    "ECHO",
]  # Asterisk as first byte; int for num elements in array; CRLF; each RESP
# def handle_data(data):
#     resp = "-ERR unknown command\r\n"
#     #    print(f"Data received {data}")
#     data_list = data.splitlines()
#     if data_list[2].decode("utf8").upper() == "PING":
#         #        print("PING received")
#         resp = REDIS_PONG
#     elif data_list[2].decode("utf8").upper() == "COMMAND":
#         resp = "*" + str(len(REDIS_COMMANDS)) + "\r\n"
#         for cmd in REDIS_COMMANDS:
#             resp += cmd
def handle_command(data):
    # set unknown command error
    resp = "-ERR unknown command" + DELIM
    data_list = data.decode("utf8").splitlines()
    num_of_items = int(data_list[0].strip("*"))  # this begins with an *
    # * <int> - number of items in array
    # $ <int> - length of command
    if DEBUG:
        print(f"Received data {data}")
    if (
        num_of_items == (len(data_list) - 1) / 2
    ):  # remove number of elements, then for each item, the length is supplied
        # Advised number of items in array matches how many we parsed
        cmd = data_list[2].upper()
        cmd_length = int(data_list[1].strip("$"))
        if not len(cmd) == cmd_length:
            # we didn't count right
            print(
                f"ERROR: advised cmd length does not match what I calculated for {cmd} != {cmd_length}"
            )
            return
        match cmd:
            case "COMMAND":
                resp = "*" + str(len(REDIS_COMMANDS)) + DELIM
                for cmd in REDIS_COMMANDS:
                    resp += "+" + cmd + DELIM
            case "PING":
                resp = REDIS_PONG
            case "ECHO":
                param = data_list[4]
                param_len = int(data_list[3].strip("$"))
                if param_len == len(param):
                    resp = "$" + str(param_len) + DELIM + param + DELIM
            case _:
                pass
    else:
        print(f"Incorrect number of elements {num_of_items}")
        resp = f"-ERR number of elements does not match: {num_of_items} <> {len(data_list) - 1}"
    return resp
def handle_client(client_socket, addr):
    print(f"Received new connection {addr}")
    if DEBUG:
        print(f"Received new connection {addr}")
    while client_socket:
        # print(f"Waiting for data from {addr}")
        data = client_socket.recv(1024)
        if len(data) > 0:
            # resp = handle_data(data)
            resp = handle_command(data)
        else:
            # print(f"Closing connection {addr}")
            return
        if resp:
            # print(f"Sending response to {addr}")
            # print(resp.encode())
            if DEBUG:
                print(f"Sending response {resp.encode()} to {addr}")
            client_socket.sendall(resp.encode())
            resp = None
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()  # wait for client
        t = Thread(target=handle_client, args=(conn, addr))
        t.start()
    server_socket.close()
if __name__ == "__main__":
    main()