from core.models import Urls, Favicons, UrlCategory
import datetime
import joblib


def getResults(query):
    results = []
    matchingUrls = []

    res_title = getResultsWithMatch("title", query)
    res_keyword = getResultsWithMatch("keyword", query)
    res_description = getResultsWithMatch("description", query)
    res_url = getResultsWithMatch("url", query)


    rankedResults = returnRankedResults(res_title, res_keyword, res_description, res_url)

    #remove duplicates based on url
    distinctResults = []
    [distinctResults.append(x[0]) for x in rankedResults if x[0] not in distinctResults]
    matchingUrls = distinctResults

    
    for mu in matchingUrls:
        url = mu.address
        if url not in results:
            icon_url = Favicons.objects.get(id=int(mu.icon_link)).icon_link
            url_category = UrlCategory.objects.get(id=int(mu.category)).category_name
            results.append({'url': url, 'title': mu.page_title, 'description': mu.page_description, 'icon_url': icon_url, 'category': url_category})

    return results



def getResultsWithMatch(param, query):
    res = []
    if param == "title":
        res = Urls.objects.filter(page_title__iregex = query)
    elif param == "keyword":
        res = Urls.objects.filter(keywords_in_it__keyword_string__iregex = query)
    elif param == "description":
        res = Urls.objects.filter(page_description__iregex = query)
    elif param == "url":
        # get only those urls which are scrapped
        res = Urls.objects.filter(address__icontains = query).exclude(last_scrapped = datetime.datetime.min)

    # try to find results with individual words in query
    words = query.split()
    if len(words) > 1:
        for word in words:
            res = res | getResultsWithMatch(param, word)
                
    #print(len(res))
    return res
        
def returnRankedResults(res_title, res_keyword, res_description, res_url):
    results = []
    wikiRanked = False
    for item in res_title:
        results.append([item, 3])
    for item in res_keyword:
        results.append([item, 2])
    for item in res_description:
        results.append([item, 2])
    for item in res_url:
        if "wikipedia." in item.address and not wikiRanked:
            results.append([item, 7])
            wikiRanked = True
        else:
            results.append([item,6])
        
    results.sort(key=lambda x: x[1]+x[0].num_of_refs*2, reverse=True)
    
    return results

def categorizeDBurls():
    urls = Urls.objects.all().exclude(last_scrapped = datetime.datetime.min)
    print("categorizing "+str(len(urls))+" urls...")
    for url in urls:
        print("categorizing "+url.address+"...")
        category = joblib.load('core/static/core/website_category_detection_model.joblib').predict([url.page_title])[0]
        url.category = UrlCategory.objects.get_or_create(category_name=category)[0].id
        url.save()
        
    print("categorization complete")

#if __name__ == "django.core.management.commands.shell":
    #categorizeDBurls()