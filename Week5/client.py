import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat,load_der_parameters, load_der_public_key
from cryptography.hazmat.primitives.asymmetric import dh

def generate_clientKeys(parameters):
    client_private_key = parameters.generate_private_key()
    client_public_key = client_private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    return client_private_key, client_public_key




def start_client():
    server = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server, port))

    parameters = client_socket.recv(2048)
    print(f' !!! Client recived parameters over public channel !!!')
    parameters = load_der_parameters(parameters)
    client_private_key, client_public_key = generate_clientKeys(parameters=parameters)
    
    server_public_key  = client_socket.recv(2048)
    server_public_key = load_der_public_key(server_public_key)
    client_socket.sendall(client_public_key)

    shared_key = client_private_key.exchange(server_public_key)
    print(f'!!! Shared key at client side !!!')
    print(shared_key.hex())
    client_socket.close()

start_client()
