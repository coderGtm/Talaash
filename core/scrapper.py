import requests
from bs4 import BeautifulSoup
import re
from core.models import Keywords, Urls

def scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # using a set data structure to store all urls on this page and avoid duplication
    link_urls_on_this_page = set()
    for link in soup.find_all('a', href = True):
        found_url = str(link.get('href'))
        if re.match(url_regex, found_url) is not None:
            link_urls_on_this_page.add(found_url)
    print(link_urls_on_this_page)


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


    # saving current url to db if not already saved, and getting its reference
    url_row, created_url_obj = Urls.objects.get_or_create(address = url)
    # save keywords to database model Keywords and relate it with current url by many-to-many relationship
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:
            keyword_row, created_keyword_obj = Keywords.objects.get_or_create(keyword = keyword)
            url_row.keywords_in_it.add(keyword_row)

    # create entries for aa links found in page and increment their num_of_refs


# regex for checking if valid url
#source: https://stackoverflow.com/a/7160778/12312757
url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


scrap('https://codergtm.github.io/')