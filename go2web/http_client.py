import socket
import ssl

GET_REQUEST_TEMPLATE = "GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

def get_url_and_ssl(url):
    if url.startswith("http://"):
        return url[7:], False
    elif url.startswith("https://"):
        return url[8:], True
    else:
        raise ValueError("Invalid URL: must start with http:// or https://")

def get_host_and_path(url):
    if "/" in url:
        host, path = url.split("/", 1)
        path = "/" + path
    else:
        host = url
        path = "/"
    return host, path

def parse_url(url):
    url, use_ssl = get_url_and_ssl(url)

    host, path = get_host_and_path(url)

    return host, path, use_ssl

def get_socket(host, use_ssl):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=host)
        sock.connect((host, 443))
    else:
        sock.connect((host, 80))
    return sock

def get_data(sock):
    response = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    return response.decode("utf-8", errors="replace")

def send_http_request(host, path, use_ssl=False):
    sock = get_socket(host, use_ssl)

    request = GET_REQUEST_TEMPLATE.format(path=path, host=host)
    sock.sendall(request.encode())
    response = get_data(sock)

    sock.close()
    return response

def redirect(headers):
    for header in headers:
        if header.lower().startswith("location:"):
            new_url = header.split(": ", 1)[1].strip()
            print(f"Redirecting to: {new_url}")
            return new_url
    return None

def http_get(url, max_redirects=5):
    if max_redirects == 0:
        raise ValueError("Error: too many redirects")
        return None, None, None

    host, path, use_ssl = parse_url(url)

    response_text = send_http_request(host, path, use_ssl)

    header_part, body = response_text.split("\r\n\r\n", 1)
    headers = header_part.split("\r\n")
    status_line = headers[0]

    status_code = int(status_line.split(" ")[1])
    if status_code in (301, 302, 303):
        new_url = redirect(headers[1:])
        if new_url:
            return http_get(new_url, max_redirects - 1)

    if status_code != 200:
        raise ValueError(f"Error: HTTP request failed with status code {status_code}")


    return status_line, headers[1:], body