import requests
from bs4 import BeautifulSoup

from core.models import Keywords, Links

def scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    links = soup.find_all('a')
    keywords = soup.find_all('meta', attrs={'name':'keywords'})

    # add headings to keywords
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for heading in headings:
        words = heading.text.split()
        for word in words:
            keywords.extend(word.split())

    # add title to keywords
    title = soup.find_all('title')
    for t in title:
        words = t.text.split()
        for word in words:
            keywords.extend(word.split())

    # save keywords to database model Keywords
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:
            keyword, created = Keywords.objects.get_or_create(keyword=keyword)
            keyword.save()

    # save current url and keywords to database model Links
    link, created = Links.objects.get_or_create(link_url=url)
    link.link_keywords.set(keywords)
    link.save()
    if created:
        link.link_ref_num = 0
    else:
        link.link_ref_num += 1

        



#scrap('https://codergtm.github.io/')