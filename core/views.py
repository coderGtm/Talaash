from django.shortcuts import render, redirect
from .forms import SearchForm
from . import engine

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
    context['form'] = form

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

    return render(request, 'search_result.html', context)

maxResultsOnPage = 10