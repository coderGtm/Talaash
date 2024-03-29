from django.shortcuts import render, redirect
from .forms import SearchForm
from . import engine
from core.models import Urls, RootDomain
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
        root_url = RootDomain.objects.all()[0].root_url
        root_title = RootDomain.objects.all()[0].root_title
    context['form'] = form
    context['totalScrappedUrls'] = totalScrappedUrls
    context['lastScrappedDate'] = lastScrappedDate
    context['root_url'] = root_url
    context['root_title'] = root_title

    return render(request, 'home.html', context)

def api_home(request):
    context = {}
    totalScrappedUrls = Urls.objects.all().exclude(last_scrapped = datetime.datetime.min).count()
    lastScrappedDate = Urls.objects.all().exclude(last_scrapped = datetime.datetime.min).order_by('-last_scrapped')[0].last_scrapped
    root_url = RootDomain.objects.all()[0].root_url
    root_title = RootDomain.objects.all()[0].root_title
    context['totalScrappedUrls'] = totalScrappedUrls
    context['lastScrappedDate'] = lastScrappedDate
    context['root_url'] = root_url
    context['root_title'] = root_title

    return JsonResponse({'totalScrappedUrls': totalScrappedUrls, 'lastScrappedDate': lastScrappedDate, 'root_url': root_url, 'root_title': root_title})

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
    if query == '':
        return redirect('/')
    start = request.GET.get('start', 0)
    context['form'] = form
    context['query'] = query
    results = engine.getResults(query)
    context['results'] = results[int(start):int(start)+maxResultsOnPage]
    context['totalResults'] = len(results)

    return render(request, 'search_result.html', context)

def api_search(request):
    context = {}
    query = request.GET.get('q','')
    if query == '':
        return JsonResponse({'results': [], 'totalResults': 0})
    start = request.GET.get('start', 0)
    context['query'] = query
    results = engine.getResults(query)
    context['results'] = results[int(start):int(start)+maxResultsOnPage]
    context['totalResults'] = len(results)

    return JsonResponse({'results': context['results'], 'totalResults': context['totalResults']})


maxResultsOnPage = 10
