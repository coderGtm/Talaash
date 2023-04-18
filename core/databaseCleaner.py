from random import shuffle
from core.models import Keywords, Urls
import datetime

# clean database of some unscrapped urls

def cleanDatabaseOfUnscrappedURLs(percent):
    '''delete given percentage of unscrapped urls from database randomly'''

    print("[+] Initializing cleaning of {0} of unscrapped URLS from database...".format(str(percent)+"%"))
    # get all unscrapped urls
    urls = Urls.objects.filter(last_scrapped = datetime.datetime.min)
    print("[+] Found {0} unscrapped URLs in database before cleanup.".format(len(urls)))
    print("---------------------------------------------")
    # shuffle urls
    urls = list(urls)
    shuffle(urls)
    # delete given % of urls
    urls_to_delete = urls[:int(len(urls)*(percent/100))]
    len_urls_to_delete = len(urls_to_delete)
    print("[+] Deleting {0} unscrapped URLs from database...".format(len_urls_to_delete))
    for i in range(len_urls_to_delete):
        print("[-] Deleting ({0}/{1}) URL object: {2}".format(i+1,len_urls_to_delete,urls_to_delete[i].address))
        urls_to_delete[i].delete()

    # get all unscrapped urls
    urls = Urls.objects.filter(last_scrapped = datetime.datetime.min)
    print("---------------------------------------------")
    print("[+] Deleted {0} unscrapped URLs from database.".format(len(urls_to_delete)))
    print("[+] Found {0} unscrapped URLs in database after cleanup.".format(len(urls)))
    print("[+] Done cleaning up database of unscrapped URLs.")

def cleanDatabaseOfUnreachablePages():
    '''delete all unreachable pages from database i.e urls with title as 404 Not Found or 500 Internal Server Error or 403 Forbidden or 400 Bad Request or 401 Unauthorized or 408 Request Timeout or 502 Bad Gateway or 504 Gateway Timeout or 503 Service Unavailable or 505 HTTP Version Not Supported or 410 Gone or 411 Length Required or 412 Precondition Failed or 413 Request Entity Too Large or 414 Request-URI Too Long or 415 Unsupported Media Type or 416 Requested Range Not Satisfiable or 417 Expectation Failed or 418 I'm a teapot or 421 Misdirected Request or 422 Unprocessable Entity or 423 Locked or 424 Failed Dependency or 426 Upgrade Required or 428 Precondition Required or 429 Too Many Requests or 431 Request Header Fields Too Large or 451 Unavailable For Legal Reasons or 444 No Response or 449 Retry With or 450 Blocked by Windows Parental Controls or 451 Redirect or 494 Request Header Too Large or 495 Cert Error or 496 No Cert or 497 HTTP to HTTPS or 499 Client Closed Request or 499 Token expired/invalid or 499 SSL Certificate Error or 499 SSL Certificate Required or 499 HTTP Request Sent to HTTPS Port or 499 Invalid Token or 499 Token required or 499 Incomplete Read or 499 Request Header Or Cookie Too Large or 499 Site is overloaded or 499 Retry with unverifiable HTTPS or 499 Client Closed Request or 499 Token required or 499 Token expired/invalid or 499 Incomplete Read or 499 Request Header Or Cookie Too Large or 499 Site is overloaded or 499 Retry with unverifiable HTTPS or 499 Client Closed Request or 499 Token required or 499 Token expired/invalid or 499 Incomplete Read or 499 Request Header Or Cookie Too Large or 499 Site is overloaded or 499 Retry with unverifiable HTTPS or 499 Client Closed Request or 499 Token required or 499 Token expired/invalid or 499 Incomplete Read or 499 Request Header Or Cookie Too Large or 499 Site is overloaded or 499 Retry with unverifiable HTTPS or 499 Client Closed Request or 499 Token required or 499 Token expired/invalid or 499 Incomplete Read or 499 Request Header Or Cookie Too Large or 499 Site is overloaded or 499 Retry with unverifiable HTTPS or 499 Client Closed Request or 499 Token required or 499 Token expired/invalid or 499 Incomplete Read or 499 Request Header Or Cookie Too Large'''
    print("[+] Initializing cleaning of unreachable pages from database...")
    prevCount = len(Urls.objects.all())
    # get all unreachable pages
    Urls.objects.filter(page_title__contains = "404 Not Found").delete()
    Urls.objects.filter(page_title__contains = "500 Internal Server Error").delete()
    Urls.objects.filter(page_title__contains = "403 Forbidden").delete()
    Urls.objects.filter(page_title__contains = "400 Bad Request").delete()
    Urls.objects.filter(page_title__contains = "401 Unauthorized").delete()
    Urls.objects.filter(page_title__contains = "408 Request Timeout").delete()
    Urls.objects.filter(page_title__contains = "502 Bad Gateway").delete()
    Urls.objects.filter(page_title__contains = "504 Gateway Timeout").delete()
    Urls.objects.filter(page_title__contains = "503 Service Unavailable").delete()
    Urls.objects.filter(page_title__contains = "505 HTTP Version Not Supported").delete()
    Urls.objects.filter(page_title__contains = "410 Gone").delete()
    Urls.objects.filter(page_title__contains = "411 Length Required").delete()
    Urls.objects.filter(page_title__contains = "412 Precondition Failed").delete()
    Urls.objects.filter(page_title__contains = "413 Request Entity Too Large").delete()
    Urls.objects.filter(page_title__contains = "414 Request-URI Too Long").delete()
    Urls.objects.filter(page_title__contains = "415 Unsupported Media Type").delete()
    Urls.objects.filter(page_title__contains = "416 Requested Range Not Satisfiable").delete()
    Urls.objects.filter(page_title__contains = "417 Expectation Failed").delete()
    Urls.objects.filter(page_title__contains = "418 I'm a teapot").delete()
    Urls.objects.filter(page_title__contains = "421 Misdirected Request").delete()
    Urls.objects.filter(page_title__contains = "422 Unprocessable Entity").delete()
    Urls.objects.filter(page_title__contains = "423 Locked").delete()
    Urls.objects.filter(page_title__contains = "424 Failed Dependency").delete()
    Urls.objects.filter(page_title__contains = "426 Upgrade Required").delete()
    Urls.objects.filter(page_title__contains = "428 Precondition Required").delete()
    Urls.objects.filter(page_title__contains = "429 Too Many Requests").delete()
    Urls.objects.filter(page_title__contains = "431 Request Header Fields Too Large").delete()
    Urls.objects.filter(page_title__contains = "451 Unavailable For Legal Reasons").delete()
    Urls.objects.filter(page_title__contains = "444 No Response").delete()
    Urls.objects.filter(page_title__contains = "449 Retry With").delete()
    Urls.objects.filter(page_title__contains = "450 Blocked by Windows Parental Controls").delete()
    Urls.objects.filter(page_title__contains = "451 Redirect").delete()
    Urls.objects.filter(page_title__contains = "494 Request Header Too Large").delete()
    Urls.objects.filter(page_title__contains = "495 Cert Error").delete()
    Urls.objects.filter(page_title__contains = "496 No Cert").delete()
    Urls.objects.filter(page_title__contains = "497 HTTP to HTTPS").delete()
    Urls.objects.filter(page_title__contains = "499 Client Closed Request").delete()
    Urls.objects.filter(page_title__contains = "499 Token expired/invalid").delete()
    Urls.objects.filter(page_title__contains = "499 SSL Certificate Error").delete()
    Urls.objects.filter(page_title__contains = "499 SSL Certificate Required").delete()
    Urls.objects.filter(page_title__contains = "499 HTTP Request Sent to HTTPS Port").delete()

    afterCount = len(Urls.objects.all())
    print("[+] Deleted {0} unreachable pages from database.".format(prevCount - afterCount))
    print("[+] Done cleaning up database of unreachable pages.")


if __name__ == "django.core.management.commands.shell":
    #cleanDatabaseOfUnscrappedURLs(99)
    cleanDatabaseOfUnreachablePages()