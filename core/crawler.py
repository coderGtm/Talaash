import requests
from bs4 import BeautifulSoup, Comment
import re
import datetime
from urllib.parse import urljoin
from core.models import Keywords, Urls, Favicons, UrlCategory, RootDomain
from random import shuffle
import joblib

def scrap(url: str):
    if isUrlAllowed(url) == False:
        return (None, None, None, None, None, None)
    try:
        page = requests.get(url, timeout = 10)
    except:
        return (None, None, None, None, None, None)
    if page.status_code != 200:
        print("Error: ", page.status_code)
        return (None, None, None, None, None, None)
    docParser = ''
    if url[-4:] == '.pdf' or url[-4:] == '.doc' or url[-5:] == '.docx' or url[-4:] == '.ppt' or url[-5:] == '.pptx' or url[-4:] == '.xls' or url[-5:] == '.xlsx':
        docParser = 'lxml'
        content = page.content
    else:
        docParser = 'html.parser'
        content = page.text

    soup = BeautifulSoup(content, docParser)
    
    # using Set data structure to store all urls on this page and avoid duplication
    urls_found_on_this_page = set()
    for link in soup.find_all('a', href = True):
        found_url = str(link.get('href'))
        if len(found_url) > 0:
            if found_url[0] == "/":
                found_url = urljoin(url,found_url)
            if found_url != url and re.match(url_regex, found_url) is not None:
                urls_found_on_this_page.add(found_url)
    
    urls_found_on_this_page = list(urls_found_on_this_page)

    keywords = []
    
    if soup.find_all('meta', attrs={'name':'description'}):
        scrapped_desc = soup.find('meta', attrs={'name':'description'}).get("content")
        keywords.append(scrapped_desc)
        page_description = soup.find('meta', attrs={'name':'description'}).get("content")
    else:
        page_description = None

    # add headings to keywords
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for heading in headings:
        keywords.append(str(heading.text).strip())
    if page_description == None:
        if headings:
            page_description = headings[0].text.strip()
        else:
            page_description = text_from_html(content)[:pageDescriptionCharLimit]

    # add title to keywords and save page title
    page_title = None
    titles = soup.find_all('title')
    for title in titles:
        keywords.append(str(title.text).strip())

    if len(titles) == 0:
        page_title = text_from_html(content)[:pageTitleCharLimit]
    else:
        page_title = titles[0].text.strip()

    iconLink = getFavicon(url, soup)

    # categorize url based on its content
    urlCategory = joblib.load('core/static/core/website_category_detection_model.joblib').predict([text_from_html(content[:2500])])[0]

    return (keywords, page_title, page_description, iconLink, urls_found_on_this_page, urlCategory)



def store(url, keywords, urls_found_on_this_page, title, description, iconLink, urlCategory):
    # saving current url to db if not already saved, and getting its reference, later mapping it with keywords and updating its last_scrapped value
    url_row, created_url_obj = Urls.objects.get_or_create(address = url)
    #delete keywords feild entry as some keywords may no longer be in page so start afresh
    url_row.keywords_in_it.clear()
    # update or create title, description, iconLink and category
    url_row.page_title = title[:pageTitleCharLimit]
    url_row.page_description = description[:pageDescriptionCharLimit]
    favicon_row = Favicons.objects.get_or_create(icon_link = iconLink)
    url_row.icon_link = str(favicon_row[0].id)
    url_row.category = UrlCategory.objects.get_or_create(category_name = urlCategory)[0].id
    # save keywords to database model Keywords and relate it with current url by many-to-many relationship
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:
            keyword_row, created_keyword_obj = Keywords.objects.get_or_create(keyword_string = keyword)
            url_row.keywords_in_it.add(keyword_row)     # Adding a second time is OK, it will not duplicate the relation

    # create entries for all links found in page, and increment their num_of_refs if this url is not earlier scrapped
    # i.e increment iff current url is not yet scrapped and link is already present in db (as default is 1)
    # not yet scrapped can be determined by last_scrapped being datetime.datetime.min
    for link in urls_found_on_this_page:
        if isUrlAllowed(link):
            link_row, created_link_obj = Urls.objects.get_or_create(address = link)
            if (not created_link_obj) and url_row.last_scrapped == datetime.datetime.min:
                link_row.num_of_refs += 1
                link_row.save()
    
    url_row.last_scrapped = datetime.datetime.utcnow()
    url_row.save()

def getFavicon(url, soup):
    icon_link = soup.find("link", rel="shortcut icon")
    if icon_link is None:
        icon_link = soup.find("link", rel="icon")
    if icon_link is None:
        return getBaseUrl(url) + '/favicon.ico'
    if not icon_link["href"].startswith("http"):
        return urljoin(getBaseUrl(url),icon_link["href"])
    return icon_link["href"]

def getBaseUrl(url):
    return re.match(r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', url, re.IGNORECASE).group(0)

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

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def getUrlsFromSitemap(sitemapUrl):
    urls = []
    sitemap = requests.get(sitemapUrl)
    if sitemap.status_code == 200:
        soup = BeautifulSoup(sitemap.content, 'xml')
        for url in soup.find_all('url'):
            urls.append(url.find('loc').text)
    return urls

def isUrlAllowed(url):
    allowed_domains = [rootDomain, "https://isc.charusat.ac.in", "https://charusat.edu.in:912/"]
    url = url.strip().lower()
    if url[-4:] == '.pdf' or url[-4:] == '.doc' or url[-5:] == '.docx' or url[-4:] == '.ppt' or url[-5:] == '.pptx' or url[-4:] == '.xls' or url[-5:] == '.xlsx':
        return False # return None if url is a document as currently we are not supporting documents
    if url[-4:] == '.jpg' or url[-4:] == '.png' or url[-4:] == '.gif' or url[-4:] == '.svg' or url[-4:] == '.bmp' or url[-4:] == '.ico':
        return False
    if url[-4:] == '.mp3' or url[-4:] == '.mp4' or url[-4:] == '.wav' or url[-4:] == '.avi' or url[-4:] == '.flv' or url[-4:] == '.wmv':
        return False
    if url[-4:] == '.zip' or url[-4:] == '.rar' or url[-4:] == '.7z' or url[-4:] == '.tar' or url[-4:] == '.gz' or url[-4:] == '.bz2':
        return False
    if url[-4:] == '.exe' or url[-4:] == '.msi' or url[-4:] == '.apk' or url[-4:] == '.dmg' or url[-4:] == '.deb' or url[-4:] == '.rpm':
        return False
    if url[-4:] == '.ttf' or url[-4:] == '.otf' or url[-4:] == '.woff' or url[-4:] == '.woff2' or url[-4:] == '.eot':
        return False
    if url[-4:] == '.css' or url[-3:] == '.js':
        return False
    if url[-4:] == '.xml' or url[-4:] == '.rss':
        return False
    if url[-4:] == '.csv' or url[-4:] == '.txt' or url[-4:] == '.log':
        return False
    
    if domainRestricted:
        flag = False
        for domain in allowed_domains:
            if url.find(domain) == 0:
                flag = True
        return flag
        
    return True


if __name__ == "django.core.management.commands.shell":
    url_regex = get_url_regex()
    pageTitleCharLimit = 60
    pageDescriptionCharLimit = 140
    maxUrlsToScrapInSession = 10
    urlsScrappedInSession = 0
    scrapIntervalInDays = 3
    manualAddition = True
    domainRestricted = True
    parseSitemap = True
    rootDomain = "https://charusat.ac.in/"
    rootTitle = "Charotar University of Science and Technology"
    sitemapUrl = "https://charusat.ac.in/sitemap.xml"

    if domainRestricted:
        RootDomain.objects.all().delete()
        record, created_now = RootDomain.objects.get_or_create(root_url = rootDomain)
        record.root_title = rootTitle
        record.save()

    print("[ + ] Initializing crawler!")
    print("[ + ] Scraping {0} urls in this session which are not scrapped in the last {1} days.".format(maxUrlsToScrapInSession, scrapIntervalInDays))
    print("-------------------------------------------\n")

    if domainRestricted and parseSitemap:
        print("[ + ] Parsing sitemap for urls in domain '{0}'".format(rootDomain))
        urlsInSitemap = getUrlsFromSitemap(sitemapUrl)
        print("[ + ] Found {0} urls in sitemap.".format(len(urlsInSitemap)))
        urlsAddedFromSitemap = 0
        for url in urlsInSitemap:
            if isUrlAllowed(url):
                link_row, created_link_obj = Urls.objects.get_or_create(address = url)
                if created_link_obj:
                    link_row.num_of_refs = 0
                    link_row.save()
                    urlsAddedFromSitemap += 1
        print("[ + ] Added {0} urls to database from sitemap.".format(urlsAddedFromSitemap))

    if manualAddition:
        url_to_scrap = "https://charusat.ac.in/"
        keywords_found_on_this_page, page_title, page_description, iconLink, urls_found_on_this_page, category = scrap(url_to_scrap)
        if (keywords_found_on_this_page, urls_found_on_this_page) == (None, None):
            print("[ - ] The manual addition URL '{0}' cannot be scrapped.".format(url_to_scrap))
        else:
            store(url_to_scrap, keywords_found_on_this_page, urls_found_on_this_page, page_title, page_description, iconLink, category)
            urlsScrappedInSession += 1
            print("[ + ] Crawled ({0}/{1}) URL: {2}".format(urlsScrappedInSession,maxUrlsToScrapInSession,url_to_scrap))

    while urlsScrappedInSession < maxUrlsToScrapInSession:
        to_scrap_urls = list(Urls.objects.filter(last_scrapped__lt = (datetime.datetime.utcnow() - datetime.timedelta(days = scrapIntervalInDays))))
        if len(to_scrap_urls) == 0:
            print("[ - ] No URLs to scrap currenty. Try changing scrap conditions or manually add new URLs.")
            break
        shuffle(to_scrap_urls)      # shuffling to ge more diversified results
        for i in range(len(to_scrap_urls)):
            url_object = to_scrap_urls[i]
            if urlsScrappedInSession >= maxUrlsToScrapInSession:
                break
            url_to_scrap = url_object.address
            keywords_found_on_this_page, page_title, page_description, iconLink, urls_found_on_this_page, category = scrap(url_to_scrap)
            if (keywords_found_on_this_page, urls_found_on_this_page) == (None, None):
                print("[ - ] Skipping URL: {0}".format(url_to_scrap))
                continue
            store(url_to_scrap, keywords_found_on_this_page, urls_found_on_this_page, page_title, page_description, iconLink, category)
            urlsScrappedInSession += 1
            print("[ + ] Crawled ({0}/{1}) URL: {2}".format(urlsScrappedInSession,maxUrlsToScrapInSession,url_to_scrap))

    print("\n-------------------------------------------")
    print("[ + ] Total Keywords string in Database: ", Keywords.objects.count())
    print("[ + ] Total URLs present in Database: ",Urls.objects.count())
    print("[ + ] Total URLs crawled: ",Urls.objects.exclude(last_scrapped = datetime.datetime.min).count())