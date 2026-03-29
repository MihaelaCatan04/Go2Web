import socket
import ssl
from cache import get_from_cache, get_conditional_headers, store_in_cache, get_cache_entry
import time
from content_handler import format_response

GET_REQUEST_TEMPLATE = (
    "GET {path} HTTP/1.1\r\n"
    "Host: {host}\r\n"
    "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36\r\n"
    "Accept: application/json, text/html, */*\r\n"
    "Accept-Language: en-US,en;q=0.9\r\n"
    "Connection: close\r\n"
    "\r\n"
)

def find_chunk_size(raw):
    crlf_pos = raw.find(b"\r\n")
    if crlf_pos == -1:
        return None, None
    
    size_str = raw[:crlf_pos].decode().strip()
    if ";" in size_str:
        size_str = size_str.split(";")[0]
    
    try:
        chunk_size = int(size_str, 16)
    except ValueError:
        return None, None
    
    return chunk_size, crlf_pos


def extract_chunk(raw, crlf_pos, chunk_size):
    chunk_start = crlf_pos + 2
    chunk_end = chunk_start + chunk_size
    chunk_data = raw[chunk_start:chunk_end]
    remaining = raw[chunk_end + 2:]
    return chunk_data, remaining


def decode_chunked(body):
    decoded = b""

    if isinstance(body, str):
        raw = body.encode("utf-8", errors="replace")
    else:
        raw = body

    while raw:
        chunk_size, crlf_pos = find_chunk_size(raw)
        if chunk_size is None:
            break
        if chunk_size == 0:
            break

        chunk_data, raw = extract_chunk(raw, crlf_pos, chunk_size)
        decoded += chunk_data

    return decoded.decode("utf-8", errors="replace")

def is_chunked(headers):
    for header in headers:
        if header.lower().startswith("transfer-encoding:") and "chunked" in header.lower():
            return True
    return False

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
    sock.settimeout(10)
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

def send_http_request(host, path, use_ssl=False, extra_headers=""):
    sock = get_socket(host, use_ssl)

    request = GET_REQUEST_TEMPLATE.format(path=path, host=host)
    if extra_headers:
        request = request[:-2] + extra_headers + "\r\n"
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
    cached = get_from_cache(url)
    if cached:
        return cached

    if max_redirects == 0:
        raise ValueError("Error: too many redirects")

    host, path, use_ssl = parse_url(url)

    extra_headers = get_conditional_headers(url)

    response_text = send_http_request(host, path, use_ssl, extra_headers)

    header_part, body = response_text.split("\r\n\r\n", 1)
    headers = header_part.split("\r\n")
    status_line = headers[0]

    status_code = int(status_line.split(" ")[1])
    if status_code in (301, 302, 303):
        new_url = redirect(headers[1:])
        if new_url:
            return http_get(new_url, max_redirects - 1)

    if status_code == 304:
        entry = get_cache_entry(url)
        if entry:
            print("Server confirmed content unchanged (304)")
            entry["timestamp"] = time.time()
            store_in_cache(url, entry["status_line"], entry["headers"], entry["body"])
            return entry["status_line"], entry["headers"], entry["body"]

    if is_chunked(headers[1:]):
        body = decode_chunked(body)
    
    if 200 <= status_code < 300:
        store_in_cache(url, status_line, headers[1:], body)


    return status_line, headers[1:], body