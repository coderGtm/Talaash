from core.models import Keywords, Urls

def getResults(query):
    results = []
    matchingUrls = []

    for item in Keywords.objects.filter(keyword_string__contains = query):
        for q in Urls.objects.filter(keywords_in_it__exact = item.id):
            matchingUrls.append([q.address, q.num_of_refs])
            
    matchingUrls.sort(key=getNumOfRefs, reverse=True)
    
    for mu in matchingUrls:
        url = mu[0]
        if url not in results:
            results.append(url)
            print(url)


def getNumOfRefs(elem):
    return elem[1]

getResults("mahabharat")