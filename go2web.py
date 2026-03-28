import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect(("example.com", 80))

request = "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"

socket.sendall(request.encode())

response = b""
while True:
    data = socket.recv(1024)
    if not data:
        break
    response += data

socket.close()
print(response.decode())