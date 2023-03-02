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
    context['form'] = form
    context['query'] = query
    context['results'] = engine.getResults(query)
    print(context['results'])
    return render(request, 'search_result.html', context)