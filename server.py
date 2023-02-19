import socket
import sys
import os
from dotenv import load_dotenv


load_dotenv()

server_address = (os.getenv('HOST'), int(os.getenv('PORT')))

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_server.bind(server_address)
socket_server.listen()

while True:
    try:
        print('Wait connection...')
        client_connection, client_address = socket_server.accept()

    except KeyboardInterrupt:
        socket_server.close()
        print(end='\r')
        sys.exit()

    try:
        print('Connected:', client_address)

        while True:
            data = client_connection.recv(1024)
            print(f'Information received {data.decode("utf-8")}')

            if data:
                print('Data processing')
                print('Sending to the client')
                data = data.decode('utf-8')
                data = data.upper().encode('utf-8')
                client_connection.sendall(
                    'Response: '.encode('utf-8') + data
                )
            else:
                print('No data from', client_address)
                break

    except KeyboardInterrupt:
        socket_server.close()
        print(end='\r')
        sys.exit()
