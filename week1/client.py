import socket


def client_program():
    host = '127.0.0.1' 
    port = 5005  # socket server port number

    try:
        client_socket = socket.socket()
    except:
        print('Unable to open connection')
        print(f'Reason {str(client_socket.error)}')
        
    client_socket.connect((host, port))  

    message = input(" -> ")  

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  
        data = client_socket.recv(1024).decode()  

        print('Received from server: ' + data)  

        message = input(" -> ")  

    client_socket.close()  


if __name__ == '__main__':
    client_program()