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


if __name__ == "django.core.management.commands.shell":
    cleanDatabaseOfUnscrappedURLs(90)