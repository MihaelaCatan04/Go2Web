import socket
from url_parser import parse_url

GET_REQUEST_TEMPLATE = "GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

def send_http_request(host, path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 80))

    request = GET_REQUEST_TEMPLATE.format(path=path, host=host)
    sock.sendall(request.encode())

def receive_http_response(sock):
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk

    sock.close()
    return response.decode()


def http_get(url):
    host, path = parse_url(url)

    send_http_request(host, path)
    response = receive_http_response(sock)


    response_text = response.decode()
    header_part, body = response_text.split("\r\n\r\n", 1)
    headers = header_part.split("\r\n")
    status_line = headers[0]

    return status_line, headers[1:], body