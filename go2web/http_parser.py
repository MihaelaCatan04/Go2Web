def split_response(response_text):
    parts = response_text.split("\r\n\r\n", 1)
    if len(parts) != 2:
        raise ValueError("Invalid HTTP response: could not separate headers and body")

    header_part, body = parts
    headers = header_part.split("\r\n")
    status_line = headers[0]
    return status_line, headers[1:], body


def get_status_code(status_line):
    parts = status_line.split(" ")
    if len(parts) < 2 or not parts[1].isdigit():
        raise ValueError("Invalid HTTP status line")
    return int(parts[1])


def is_chunked(headers):
    for header in headers:
        if header.lower().startswith("transfer-encoding:") and "chunked" in header.lower():
            return True
    return False


def find_chunk_size(raw):
    crlf_pos = raw.find(b"\r\n")
    if crlf_pos == -1:
        return None, None

    size_str = raw[:crlf_pos].decode("utf-8", errors="replace").strip()

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


def get_redirect_location(headers):
    for header in headers:
        if header.lower().startswith("location:"):
            return header.split(": ", 1)[1].strip()
    return None