import socket
import sys

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

response_text = response.decode()

header, body = response_text.split("\r\n\r\n", 1)

print("Headers:")
print(header)
print("Body:")
print(body)

def print_help():
    print("Usage: python go2web.py")
    print("go2web -u <URL>         -> fetch a URL")
    print("go2web -s <search-term> -> search the web")
    print("go2web -h               -> show this help")

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        print_help()
        return

    if sys.argv[1] == "-u":
        if len(sys.argv) < 3:
            print("Error: URL not provided")
            return
        url = sys.argv[2]
        print(f"Fetching URL: {url}")
        # TODO Implement URL fetching logic here

    if sys.argv[1] == "-s":
        if len(sys.argv) < 3:
            print("Error: Search term not provided")
            return
        search_term = " ".join(sys.argv[2:])
        print(f"Searching for: {search_term}")
        # TODO Implement web search logic here

    if sys.argv[1] not in ["-u", "-s", "-h"]:
        print("Error: Invalid option")
        print_help()

if __name__ == "__main__":
    main()