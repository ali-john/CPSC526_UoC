import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8080))

    while True:
        password = input("Enter password to send to the server (or press Enter to exit): ")

        if not password:
            break  # Break the loop if no password is provided

        client.send(password.encode())

    client.close()

if __name__ == "__main__":
    main()
