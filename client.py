import os
import socket
import sys
from time import sleep
from dotenv import load_dotenv

load_dotenv()

server_address = (os.getenv('HOST'), int(os.getenv('PORT')))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(1)
client_socket.connect(server_address)

stdin_msg = sys.stdin
stdout_msg = sys.stdout

while True:
    try:
        for line in stdin_msg:
            if 'exit' == line.strip():
                sys.exit()

            else:
                msg = line
                client_socket.sendall(msg.encode('utf-8'))

                amount_received = 0
                amount_expected = len(msg)

                while amount_received < amount_expected:

                    data = client_socket.recv(1024)
                    amount_received += len(data)
                    message = data.decode('utf-8')

                    for msg in message:
                        stdout_msg.flush()
                        sleep(0.3)
                        stdout_msg.write(msg)

    except KeyboardInterrupt:
        client_socket.close()
        print(end='\r')
        sys.exit()
