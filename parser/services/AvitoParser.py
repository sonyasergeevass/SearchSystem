from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from parser.services.BaseParser import BaseParser


class AvitoParser(BaseParser):
    def __init__(self, driver):
        super().__init__(driver, platform='avito')

    def get_search_url(self):
        return "https://www.avito.ru/"

    def parse_page(self):
        results = []
        try:
            items = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['item'])
            for item in items:
                result = {
                    'title': 'Название временно недоступно',
                    'price': 'Цена временно недоступна',
                    'link': 'Ссылка временно недоступна',
                    'source': 'Avito'  # Исправлено с Youla на Avito
                }

                # Парсим название
                try:
                    result['title'] = item.find_element(
                        By.CSS_SELECTOR,
                        self.selectors['title']
                    ).text.strip()
                except NoSuchElementException:
                    pass

                # Парсим цену
                try:
                    result['price'] = item.find_element(
                        By.CSS_SELECTOR,
                        self.selectors['price']
                    ).text.strip()
                except NoSuchElementException:
                    pass

                # Парсим ссылку
                try:
                    result['link'] = item.find_element(
                        By.CSS_SELECTOR,
                        self.selectors['link']
                    ).get_attribute('href')
                except NoSuchElementException:
                    pass

                results.append(result)

        except Exception as e:
            print(f"Ошибка при парсинге страницы Авито: {e}")

        return results