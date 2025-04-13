import multiprocessing
from django.shortcuts import render
from .forms import SearchForm
from .services.run_parser import run_parser
from .services.AuParser import AuParser
from .services.AvitoParser import AvitoParser
from .services.YoulaParser import YoulaParser

RESULTS_DIR = 'search_results'

def search_view(request):
    results = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            parsers = [
                (YoulaParser, "youla"),
                (AvitoParser, "avito"),
                (AuParser, "24au"),
            ]

            manager = multiprocessing.Manager()
            result_queue = manager.Queue()
            processes = []

            for parser_class, name in parsers:
                p = multiprocessing.Process(
                    target=run_parser,
                    args=(parser_class, query, name, result_queue)
                )
                processes.append(p)
                p.start()

            for p in processes:
                p.join()

            while not result_queue.empty():
                name, data = result_queue.get()
                results[name] = data
    else:
        form = SearchForm()

    return render(request, 'parser/search.html', {'form': form, 'results': results})