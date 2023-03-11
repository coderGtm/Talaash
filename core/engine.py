from core.models import Keywords, Urls
import datetime

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
            results.append({'url': url, 'title': mu.page_title, 'description': mu.page_description, 'icon_url': mu.icon_link})

    return results



def getResultsWithMatch(param, query):
    res = []
    if param == "title":
        res = Urls.objects.filter(page_title__icontains = query)
    elif param == "keyword":
        res = Urls.objects.filter(keywords_in_it__keyword_string__icontains = query)
    elif param == "description":
        res = Urls.objects.filter(page_description__icontains = query)
    elif param == "url":
        # get only those urls which are scrapped
        res = Urls.objects.filter(address__icontains = query).exclude(last_scrapped = datetime.datetime.min)

    # try to find results with individual words in query
    words = query.split()
    if len(words) > 1:
        for word in words:
            res = res | getResultsWithMatch(param, word)
                
    return res
        
def returnRankedResults(res_title, res_keyword, res_description, res_url):
    results = []
    for item in res_title:
        results.append([item, 4])
    for item in res_keyword:
        results.append([item, 3])
    for item in res_description:
        results.append([item, 2])
    for item in res_url:
        results.append([item, 1])
    results.sort(key=lambda x: 2*x[1]+x[0].num_of_refs, reverse=True)
    return results