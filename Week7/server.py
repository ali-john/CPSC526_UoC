import socket
import threading
import hashlib

server_password = "123"
hashed_password = hashlib.sha256(server_password.encode()).hexdigest()

correct_password_received = False
lock = threading.Lock()

def handle_client(client_socket):
    global correct_password_received
    while True:
        client_password = client_socket.recv(1024).decode()

        if not client_password:
            break  # Break the loop if no data is received

        if hashlib.sha256(client_password.encode()).hexdigest() == hashed_password:
            print("Password matched. Server loop will break.")
            with lock:
                print('dome')
                correct_password_received = True
            client_socket.close()
            break
        else:
            print("Incorrect password.")


def main():
    global correct_password_received
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen(5)
    print("Server listening on port 8080...")

    while correct_password_received == False:
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
    server.close()
    print("breaking server")
    

if __name__ == "__main__":
    main()
