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

    print("------Talaash Results for {0}-------".format(query))
    
    for mu in matchingUrls:
        url = mu[0]
        if url not in results:
            results.append(url)
            print(url)
            print(mu[1])
            print(mu[2])
            print(mu[3])
            print(mu[4])
            print("-------------------------------------------")


def getNumOfRefs(elem):
    return elem[1]

getResults("India")