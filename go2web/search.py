from bs4 import BeautifulSoup

from http_client import http_get

URL_TEMPLATE = "https://search.brave.com/search?q={query}"


def return_results(body):
    soup = BeautifulSoup(body, "html.parser")

    results = []
    for item in soup.find_all("div", class_="snippet"):
        link_tag = item.find("a")
        title_tag = item.find("div", class_="title")

        if not link_tag or not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        href = link_tag.get("href", "")

        if title and href.startswith("http"):
            results.append((title, href))

        if len(results) >= 10:
            break

    return results


def search(search_term):
    query = search_term.replace(" ", "+")
    url = URL_TEMPLATE.format(query=query)

    status_line, headers, body = http_get(url)
    return return_results(body)