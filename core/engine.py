from core.models import Keywords, Urls

def getResults(query):
    results = []
    matchingUrls = []

    for item in Keywords.objects.filter(keyword_string__contains = query):
        for q in Urls.objects.filter(keywords_in_it__exact = item.id):
            matchingUrls.append([q.address, q.num_of_refs, q.page_title, q.page_description, q.icon_link])

    individualWords = query.split(" ")
    for word in individualWords:
        for item in Keywords.objects.filter(keyword_string__contains = word):
            for q in Urls.objects.filter(keywords_in_it__exact = item.id):
                matchingUrls.append([q.address, q.num_of_refs, q.page_title, q.page_description, q.icon_link])
            
    matchingUrls.sort(key=getNumOfRefs, reverse=True)

    #remove duplicates based on url
    res = []
    [res.append(x) for x in matchingUrls if x[0] not in [y[0] for y in res]]
    matchingUrls = res
    
    for mu in matchingUrls:
        url = mu[0]
        if url not in results:
            results.append({'url': url, 'title': mu[2], 'description': mu[3], 'icon_url': mu[4]})

    return results


def getNumOfRefs(elem):
    return elem[1]

