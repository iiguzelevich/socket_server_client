import socket
import sys
import os
from time import sleep

from dotenv import load_dotenv

load_dotenv()

server_address = (os.getenv('HOST'), int(os.getenv('PORT')))

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_server.bind(server_address)
socket_server.listen()

stdout_msg_to_client = sys.stdout

while True:
    try:
        stdout_msg_to_client.write('Wait connection...\n')
        client_connection, client_address = socket_server.accept()

    except KeyboardInterrupt:
        socket_server.close()
        sys.exit()

    try:
        stdout_msg_to_client.write('Connected: ')
        stdout_msg_to_client.write(str(client_address) + '\n')
        while True:
            data = client_connection.recv(1024)
            stdout_msg_to_client.write('Information received: \n')
            message = data.decode("utf-8")
            for msg in message:
                stdout_msg_to_client.flush()
                sleep(0.3)
                stdout_msg_to_client.write(msg)

            if data:
                stdout_msg_to_client.write(
                    'Data processing\nSending to the client\n'
                )
                data = data.decode('utf-8')
                data = data.upper().encode('utf-8')
                client_connection.sendall(
                    'Response: '.encode('utf-8') + data
                )
            else:
                stdout_msg_to_client.write('No data')
                break

    except KeyboardInterrupt:
        socket_server.close()
        sys.exit()

