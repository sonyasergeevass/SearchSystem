from django.core.exceptions import ObjectDoesNotExist
from selenium.webdriver.common.by import By

from parser.models import Selector

class BaseParser:
    def __init__(self, driver, platform):
        self.driver = driver
        self.platform = platform
        self.selectors = self.load_selectors()

    def load_selectors(self):
        try:
            selector = Selector.objects.get(platform=self.platform)
            return {
                'search_box': selector.search_box,
                'next_button': selector.next_button,
                'search_button': selector.search_button,
                'item': selector.item,
                'title': selector.title,
                'price': selector.price,
                'link': selector.link,
            }
        except ObjectDoesNotExist:
            raise ValueError(f"Селекторы для платформы '{self.platform}' не найдены в базе данных")

    def search(self, query):
        self.driver.get(self.get_search_url())
        self.search_items(query)
        results = []

        results.extend(self.parse_page())
        # while True:
        #     results.extend(self.parse_page())
        #     if not self.next_page():
        #         break
        return results

    def get_search_url(self):
        raise NotImplementedError("Метод get_search_url должен быть реализован в подклассе")

    def search_items(self, query):
        search_input = self.driver.find_element(By.CSS_SELECTOR, self.selectors['search_box'])
        search_input.clear()
        search_input.send_keys(query)

        search_button = self.driver.find_element(By.CSS_SELECTOR, self.selectors['search_button'])
        search_button.click()

    def parse_page(self):
        raise NotImplementedError("Метод parse_page должен быть реализован в подклассе")

    def next_page(self):
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, self.selectors['next_button'])
            next_button.click()
            return True
        except Exception:
            return False