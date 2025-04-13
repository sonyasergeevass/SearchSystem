import json
import os
import traceback
from multiprocessing import Queue
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

RESULTS_DIR = 'search_results'
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_parser(parser_class, query, result_key, queue: Queue):
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        driver = uc.Chrome(version_main=134, options=options)
        parser = parser_class(driver)
        result = parser.search(query)
        driver.quit()

        result_file = os.path.join(RESULTS_DIR, f"{result_key}_results.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        queue.put((result_key, result))
    except Exception as e:
        error_message = f"[{result_key}]. Ошибка: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        queue.put((result_key, []))