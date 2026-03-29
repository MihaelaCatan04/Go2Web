import json
from html_parser import strip_html


def get_content_type(headers):
    for header in headers:
        if header.lower().startswith("content-type:"):
            return header.split(": ", 1)[1].strip().lower()
    return ""


def format_json(body):
    try:
        data = json.loads(body)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return body


def format_response(headers, body):
    content_type = get_content_type(headers)

    if "application/json" in content_type:
        return format_json(body)
    elif "text/html" in content_type:
        return strip_html(body)
    else:
        return body