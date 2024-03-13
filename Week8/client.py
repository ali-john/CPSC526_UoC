# client.py

import socket
import ssl

# Server settings
HOST = 'localhost'
PORT = 12345
CERTFILE = './client/client.crt'
KEYFILE = './client/client.key'
ROOT_CA = './root/rootCA.crt'  

def main():
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    context.load_verify_locations(cafile=ROOT_CA)
    context.verify_mode = ssl.CERT_REQUIRED
    ssl_socket = context.wrap_socket(client_socket, server_hostname=HOST)
    ssl_socket.connect((HOST, PORT))

    try:
        message = input("Enter message to send (type 'quit' to exit): ")
        print(f"Sending: {message}")
        ssl_socket.sendall(message.encode())
        data = ssl_socket.recv(1024)
        print(f"Received: {data.decode()}")
    finally:
        ssl_socket.close()

if __name__ == "__main__":
    main()
