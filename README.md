# Go2Web

Go2Web is a small command-line HTTP client built for **Lab #5 – HTTP over TCP Sockets** in the Web Programming course. It implements HTTP/HTTPS over raw TCP sockets without using any high-level HTTP libraries.

## Features

- `go2web -h` – show help and usage information
- `go2web -u <URL>` – perform an HTTP(S) GET request and display a human‑readable response (no raw HTML tags)
- `go2web -s <search-term>` – search the web using a search engine and show the top 10 results (title + URL)
- Ability to follow HTTP redirects (3xx status codes)
- Simple HTTP cache backed by a JSON file (`go2web_cache.json`)
- Conditional requests using `If-Modified-Since` / `If-None-Match` when possible
- Basic content negotiation and formatting for HTML responses (stripping tags and showing only readable text)

## Installation

Requirements:

- Python 3.13 (a local virtual environment is already included in the `go2web/` folder)

Clone the repository and enter the project directory:

```bash
git clone <your-repo-url>
cd Go2Web/go2web
```

Activate the included virtual environment (optional but recommended):

```bash
source bin/activate
```

Make the `go2web.py` script executable and create a `go2web` launcher:

```bash
chmod +x go2web.py
ln -sf "$(pwd)/go2web.py" /usr/local/bin/go2web   # may require sudo
```

Now you can run the tool using the `go2web` command from anywhere.

## Usage

Show help:

```bash
go2web -h
```

Fetch and display a URL:

```bash
go2web -u https://example.com
```

Search for a term and display top 10 results:

```bash
go2web -s cats
```

After the search results are displayed, you can choose a result by entering its number to fetch and view that page via the same HTTP client.

## Implementation Details

- **No high-level HTTP libraries** – all requests are made via `socket` (and `ssl` for HTTPS) in [go2web/http_client.py](go2web/http_client.py).
- **Manual HTTP parsing** – the client constructs HTTP/1.1 GET requests, parses the status line and headers, and supports `Transfer-Encoding: chunked`.
- **Redirect handling** – 3xx responses with a `Location` header are followed up to a limited number of redirects.
- **Caching** – responses are cached in [go2web/go2web_cache.json](go2web/go2web_cache.json) using the logic from [go2web/cache.py](go2web/cache.py).
	- Each URL stores status line, headers, body, timestamp, and optionally `ETag` and `Last-Modified`.
	- Subsequent requests use conditional headers and can be served from cache when still fresh.
- **Search** – [go2web/search.py](go2web/search.py) performs a search request and parses the HTML to extract the first 10 results (title + link).
- **Content handling** – [go2web/content_handler.py](go2web/content_handler.py) and [go2web/html_parser.py](go2web/html_parser.py) strip HTML tags and present readable text in the terminal.

## Lab Requirements Mapping

- CLI with `-h`, `-u`, `-s` options ✓
- HTTP/HTTPS over raw TCP sockets (no requests/urllib/etc.) ✓
- Human‑readable responses (HTML parsed and cleaned) ✓
- Search engine integration with top 10 results ✓
- Ability to visit links from search results (extra point) ✓
- Redirect handling (extra point) ✓
- HTTP cache mechanism with conditional requests (extra points) ✓
- Basic content negotiation / handling of HTML vs. other content types (extra points) ✓

## Demo
[Too big to attach it directly here](https://drive.google.com/file/d/17qamUzCKHZuQAvU-wXrqz6YralLIoUCH/view?usp=sharing)
