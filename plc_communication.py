import socket

def client_program():
    host = socket.gethostname()  # As both code is running on the same machine
    port = 5000  # Socket server port number

    client_socket = socket.socket()  # Instantiate
    client_socket.connect((host, port))  # Connect to the server

    # Simple handshake
    message = "Hello Server"
    client_socket.send(message.encode())  # Send message

    data = client_socket.recv(1024).decode()  # Receive response
    if data :
        print('Received from server: ' + data)

    client_socket.close()  # Close the connection
    return data

if __name__ == '__main__':
    while True:
        x = client_program()
        print(x)


#program oke tinggal tambahkan setelah respons oke mau apa