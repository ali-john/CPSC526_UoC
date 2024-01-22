import socket


def server_program():

    host = '127.0.0.1' # local host
    port = 5005  
    try:
        server_socket = socket.socket()  
    except:
        print('Unable to open socket')
        print(f'Reason: {str(server_socket.error)}')


    server_socket.bind((host, port))  

    server_socket.listen(2)
      
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        while True:
            data = conn.recv(1024).decode()
            if data == 'close':
                break
            else:
                print("from connected user: " + str(data))
                message = input(' -> ')
                conn.send(message.encode())  # send data to the client

        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
