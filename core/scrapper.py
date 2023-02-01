import requests
from bs4 import BeautifulSoup
import re
import datetime
from urllib.parse import urljoin
from core.models import Keywords, Urls

def scrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # using Set data structure to store all urls on this page and avoid duplication
    urls_found_on_this_page = set()
    for link in soup.find_all('a', href = True):
        found_url = str(link.get('href'))
        if len(found_url) > 1 and found_url[0] == "/":
            found_url = urljoin(url,found_url)
            if re.match(url_regex, found_url) is not None:
                urls_found_on_this_page.add(found_url)
    
    print(urls_found_on_this_page)

    keywords = soup.find_all('meta', attrs={'name':'description'})

    # add headings to keywords
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for heading in headings:
        keywords.append(str(heading).strip())

    # add title to keywords
    titles = soup.find_all('title')
    for title in titles:
        keywords.append(str(title).strip())

    return keywords, urls_found_on_this_page



def store(url, keywords, urls_found_on_this_page):
    # saving current url to db if not already saved, and getting its reference, later mapping it with keywords and updating its last_scrapped value
    url_row, created_url_obj = Urls.objects.get_or_create(address = url)
    # save keywords to database model Keywords and relate it with current url by many-to-many relationship
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:
            keyword_row, created_keyword_obj = Keywords.objects.get_or_create(keyword = keyword)
            url_row.keywords_in_it.add(keyword_row)     # Adding a second time is OK, it will not duplicate the relation

    # create entries for all links found in page, and increment their num_of_refs if this url is not earlier scrapped
    # i.e increment iff current url is added to db this time only and link is already present in db (as default is 1)
    for link in urls_found_on_this_page:
        link_row, created_link_obj = Urls.objects.get_or_create(address = link)
        if not created_link_obj and created_url_obj:
            link_row.num_of_refs += 1
            link_row.save()
    
    url_row.last_scrapped = datetime.datetime.utcnow()
    url_row.save()



def get_url_regex():
    # regex for checking if valid url
    #source: https://stackoverflow.com/a/7160778/12312757
    return re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

if __name__ == "__main__":
    url_regex = get_url_regex()
    url = "https://github.com/coderGtm?tab=repositories"
    keywords, urls_found_on_this_page = scrap(url)
    store(url, keywords, urls_found_on_this_page)