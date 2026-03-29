import socket
import sys
from help_menu import print_help
from http_client import http_get
from html_parser import strip_html

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        print_help()
        return

    if sys.argv[1] == "-u":
        if len(sys.argv) < 3:
            print("Error: URL not provided")
            return
        url = sys.argv[2]
        status_line, headers, body = http_get(url)
        if not status_line.startswith("HTTP/1.1 200"):
            print(f"Error: Failed to fetch URL. Status: {status_line}")
            return
        strip_html_content = strip_html(body)
        print(strip_html_content)

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