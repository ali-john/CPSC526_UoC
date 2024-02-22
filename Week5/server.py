import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, ParameterFormat, load_der_parameters, load_der_public_key
from cryptography.hazmat.primitives.asymmetric import dh



def get_parameter():
    public_parameters = dh.generate_parameters(generator=2, key_size=1024)
    serialized_parameters = public_parameters.parameter_bytes(Encoding.DER, format=ParameterFormat.PKCS3)
    return public_parameters, serialized_parameters

def generate_serverKeys(parameters):
    server_private_key = parameters.generate_private_key()
    server_public_key = server_private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    return server_private_key, server_public_key

def start_talk():
    ip = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1) # listening for one connection
    print(f" Server listening on {ip}:{port} ")
    conn, addr = server_socket.accept()
    print(f"Server talking to {addr} ")

    parameters,serialized_parameters = get_parameter()
    server_private_key, server_public_key = generate_serverKeys(parameters)

    # first send the parameters over network so that clinet gets its keys
    conn.send(serialized_parameters)
    print(f'!!! Parameters sent over public channel !!!')
    # Next send server public key
    conn.sendall(server_public_key)
    print(f'!!! Sent server public key over public channel !!!')
    # recived client public key
    client_public_key = conn.recv(2048)
    client_public_key = load_der_public_key(client_public_key)

    shared_key = server_private_key.exchange(client_public_key)
    print(f'!!! Shared key at server side !!!')
    print(shared_key.hex())
    server_socket.close()
start_talk()










