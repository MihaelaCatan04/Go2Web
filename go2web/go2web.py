import socket
import sys
from help_menu import print_help
from http_client import http_get
from html_parser import strip_html
from search import search
from content_handler import format_response
import socket

def format_results(results):
    print("\nTop 10 Search Results:")
    for i, (title, href) in enumerate(results):
        print(f"{i+1}. {title}\n   {href}")

def select_result(results):
    choice = input("Enter result number to visit (or press Enter to quit): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(results):
        selected_title, selected_url = results[int(choice) - 1]
        print(f"\nFetching: {selected_url}\n")
        status_line, headers, body = http_get(selected_url)
        print(format_response(headers, body))
    elif choice:
        print("Invalid choice")

def u(arg):
    if len(arg) < 3:
        raise ValueError("Error: URL not provided")
    url = arg[2]
    status_line, headers, body = http_get(url)
    strip_html_content = strip_html(body)
    print(format_response(headers, body))

def s(arg):
    if len(arg) < 3:
        raise ValueError("Error: Search term not provided")

    search_term = " ".join(arg[2:])
    print(f"Searching for: {search_term}")
    results = search(search_term)
    if results:
        format_results(results)
        select_result(results)


def main():
    try:
        if len(sys.argv) < 2 or sys.argv[1] == "-h":
            print_help()
            return
        elif sys.argv[1] == "-u":
            u(sys.argv)
        elif sys.argv[1] == "-s":
            s(sys.argv)
        else:
            print("Error: Invalid option")
            print_help()
    except ValueError as e:
        print(f"Error: {e}")
    except ConnectionRefusedError:
        print("Error: connection refused. Is the server running?")
    except socket.gaierror:
        print("Error: could not resolve hostname. Check the URL.")
    except socket.timeout:
        print("Error: connection timed out.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()