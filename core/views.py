from django.shortcuts import render, redirect
from .forms import SearchForm
from . import engine
from core.models import Urls
import datetime
from django.http import JsonResponse

# Create your views here.

def home(request):
    context = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            return redirect('/search?q={0}'.format(query))
    else:
        form = SearchForm()
        totalScrappedUrls = Urls.objects.all().exclude(last_scrapped = datetime.datetime.min).count()
        lastScrappedDate = Urls.objects.all().exclude(last_scrapped = datetime.datetime.min).order_by('-last_scrapped')[0].last_scrapped
    context['form'] = form
    context['totalScrappedUrls'] = totalScrappedUrls
    context['lastScrappedDate'] = lastScrappedDate

    if apiMode:
        return JsonResponse({'totalScrappedUrls': totalScrappedUrls, 'lastScrappedDate': lastScrappedDate})

    return render(request, 'home.html', context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            return redirect('/search?q={0}'.format(query))
    else:
        form = SearchForm(initial={'query': request.GET.get('q','')})
    context = {}
    query = request.GET.get('q','')
    start = request.GET.get('start', 0)
    context['form'] = form
    context['query'] = query
    results = engine.getResults(query)
    context['results'] = results[int(start):int(start)+maxResultsOnPage]
    context['totalResults'] = len(results)

    if apiMode:
        return JsonResponse({'results': context['results'], 'totalResults': context['totalResults']})

    return render(request, 'search_result.html', context)

maxResultsOnPage = 10
apiMode = True