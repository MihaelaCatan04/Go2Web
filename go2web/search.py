from http_client import http_get
from bs4 import BeautifulSoup

URL_TEMPLATE = "https://html.duckduckgo.com/html/?q={query}"

def return_results(body):
    soup = BeautifulSoup(body, "html.parser")

    results = []
    for link in soup.find_all("a", class_="result__a"):
        title = link.get_text(strip=True)
        href = link.get("href")
        if title and href:
            results.append((title, href))
        if len(results) >= 10:
            break
    return results

def search(search_term):
    query = search_term.replace(" ", "+")
    url = URL_TEMPLATE.format(query=query)

    status_line, headers, body = http_get(url)

    results = return_results(body)

    return results