from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import logging

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    def __init__(self, base_url, query, selectors):
        self.base_url = base_url
        self.query = query
        self.selectors = selectors
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless")  # Запуск без окна браузера
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def _load_page(self):
        try:
            self.driver.get(self.base_url)
            time.sleep(2)  # Ожидание загрузки страницы
        except Exception as e:
            logger.error(f"Ошибка загрузки страницы {self.base_url}: {e}")
            raise

    def _enter_query(self):
        try:
            search_box = self.driver.find_element(By.CSS_SELECTOR, self.selectors['search_box'])
            search_box.clear()
            search_box.send_keys(self.query)
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)  # Ожидание загрузки результатов
        except Exception as e:
            logger.error(f"Ошибка при вводе запроса: {e}")
            raise

    @abstractmethod
    def parse_page(self):
        """ Метод парсинга страницы (определяется в подклассах) """
        pass

    def _handle_pagination(self):
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, self.selectors['next_button'])
            if next_button.is_enabled():
                next_button.click()
                time.sleep(2)  # Ожидание загрузки следующей страницы
                return True
            return False
        except Exception as e:
            logger.error(f"Ошибка пагинации: {e}")
            return False

    def run(self):
        logger.info(f"Начало парсинга {self.base_url} с запросом '{self.query}'")
        self._load_page()
        self._enter_query()

        results = []
        while True:
            try:
                results.extend(self.parse_page())
                if not self._handle_pagination():
                    break
            except Exception as e:
                logger.error(f"Ошибка при парсинге: {e}")
                break

        self.driver.quit()
        logger.info(f"Парсинг завершён, получено {len(results)} результатов")
        return results
