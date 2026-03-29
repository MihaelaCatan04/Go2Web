import socket

GET_REQUEST_TEMPLATE = "GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

def parse_url(url):
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]

    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"

    return host, path

def send_http_request(host, path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 80))

    request = GET_REQUEST_TEMPLATE.format(path=path, host=host)
    sock.sendall(request.encode())
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

    response_text = send_http_request(host, path)

    header_part, body = response_text.split("\r\n\r\n", 1)
    headers = header_part.split("\r\n")
    status_line = headers[0]

    return status_line, headers[1:], body