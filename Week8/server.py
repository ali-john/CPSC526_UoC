

import socket
import ssl

# Server settings
HOST = 'localhost'
PORT = 12345
CERTFILE = './server/server.crt'
KEYFILE = './server/server.key'
ROOT_CA = './root/rootCA.crt'  

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    context.load_verify_locations(cafile=ROOT_CA)
    context.verify_mode = ssl.CERT_REQUIRED
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server is listening on {HOST}:{PORT}...")
    
    
    while True:
        connection, client_address = server_socket.accept()
        ssl_connection = context.wrap_socket(connection, server_side=True)
        try:
            print(f"Connection from {client_address}")
            data = ssl_connection.recv(1024)
            if data:
                print(f"Received: {data.decode()}")
                ssl_connection.sendall(data) 
            else:
                break
        finally:
            ssl_connection.close()

if __name__ == "__main__":
    main()
