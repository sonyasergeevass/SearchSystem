import json
import os
from django.shortcuts import render
from .forms import SearchForm
from .services.AuParser import AuParser
from .services.AvitoParser import AvitoParser
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from .services.YoulaParser import YoulaParser

RESULTS_DIR = 'search_results'

def search_view(request):
    results = {}
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            options = Options()
            options.add_argument("--no-sandbox")  # Отключение sandbox для Docker
            options.add_argument("--disable-dev-shm-usage")  # Решение проблем с памятью
            options.add_argument("--disable-gpu")  # Отключение GPU
            driver = uc.Chrome(version_main=134, options=options)

            # Запускаем парсеры
            # youla_results = YoulaParser(driver).search(query)
            # avito_results = AvitoParser(driver).search(query)
            au24_results = AuParser(driver).search(query)

            # Сохраняем результаты в JSON
            os.makedirs(RESULTS_DIR, exist_ok=True)

            # with open(os.path.join(RESULTS_DIR, 'avito_results.json'), 'w', encoding='utf-8') as f:
            #     json.dump(avito_results, f, ensure_ascii=False, indent=4)
            # with open(os.path.join(RESULTS_DIR, 'youla_results.json'), 'w', encoding='utf-8') as f:
            #     json.dump(youla_results, f, ensure_ascii=False, indent=4)
            with open(os.path.join(RESULTS_DIR, 'au24_results.json'), 'w', encoding='utf-8') as f:
                json.dump(au24_results, f, ensure_ascii=False, indent=4)

            # Собираем результаты для отображения
            results = {
                # 'avito': avito_results,
                # 'youla': youla_results,
                 'au24': au24_results,
            }
    else:
        form = SearchForm()

    return render(request, 'parser/search.html', {'form': form, 'results': results})