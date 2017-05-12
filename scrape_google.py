import requests
from lxml import html
from bs4 import BeautifulSoup

def scrape_for_links(search_term):
    search_url_term = search_term.split(' ')
    search_url_term = '+'.join(search_url_term)
    url = 'https://www.google.com/search?hl=en&gl=us&authuser=0&tbm=nws&q=' + search_url_term + '&oq=' + search_url_term + '&gs_l=serp.3...0.0.0.4483.0.0.0.0.0.0.0.0..0.0....0...1..64.serp..0.0.0.XlgrMjaLpOg'
    req = requests.get(url)

    content = req.text
    soup = BeautifulSoup(content, 'lxml')
    links = []
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('/url?q='):
            links.append(a['href'][7:].split('&')[0])
    return links
def get_keywords_from_links(link):
    split_by_slash = link.split('/')
    keywords = []
    for slash in split_by_slash:
        split_by_dash = slash.split('-')
        if len(split_by_dash) > 1:
            for dash in split_by_dash:
                keywords.append(dash)
    return keywords

# not working :(
def scrape_for_headlines(search_term):
    search_url_term = search_term.split(' ')
    search_url_term = '+'.join(search_url_term)
    url = 'https://www.google.com/search?hl=en&gl=us&authuser=0&tbm=nws&q=' + search_url_term + '&oq=' + search_url_term + '&gs_l=serp.3...0.0.0.4483.0.0.0.0.0.0.0.0..0.0....0...1..64.serp..0.0.0.XlgrMjaLpOg'
    req = requests.get(url)
    the_html = html.fromstring(req.text)
    print(req.text)
    headlines = the_html.xpath('//h2[@class="esc-lead-article-title"] \
                                /a/span[@class="titletext"]/text()')
    print(headlines)

for link in scrape_for_links('james harden'):
    print('\n' + link)