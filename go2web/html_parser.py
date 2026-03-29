from bs4 import BeautifulSoup


def strip_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n", strip=True)