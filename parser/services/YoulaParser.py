import time

from selenium.common import NoSuchElementException, InvalidSelectorException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from parser.services.BaseParser import BaseParser


class YoulaParser(BaseParser):
    def __init__(self, driver):
        super().__init__(driver, platform='youla')

    def get_search_url(self):
        return "https://www.youla.ru/"

    def fake_mouse_activity(self):
        actions = ActionChains(self.driver)
        actions.move_by_offset(100, 100).perform()
        time.sleep(0.5)
        actions.move_by_offset(-100, -50).perform()
        time.sleep(0.5)
        print("🖱️ Имитация активности пользователя выполнена.")



    def scroll_page(self, pause_time=5, max_scrolls=3):
        """Эмулирует прокрутку страницы вниз"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for i in range(max_scrolls):
            print(f"🔽 Прокрутка {i + 1}/{max_scrolls}")
            self.driver.execute_script("window.focus();")
            self.fake_mouse_activity()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("🛑 Достигнут конец страницы")
                break
            last_height = new_height

    def parse_page(self):
        results = []
        self.scroll_page()
        # Подождем, пока элементы с параметрами будут загружены
        time.sleep(5)
        self.scroll_page()
        # Подождем, пока элементы с параметрами будут загружены
        time.sleep(5)
        items = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['item'])
        time.sleep(5)
        print(f"Найдено {len(items)} блоков")
        # with open('page_debug.html', 'w', encoding='utf-8') as f:
        #     f.write(self.driver.page_source)

        for item in items:
            html = item.get_attribute('innerHTML')
            print("HTML текущего блока:\n", html)
            print("Ищем селектор:", self.selectors['title'])

            result = {
                'title': 'Название временно недоступно',
                'price': 'Цена временно недоступна',
                'link': 'Ссылка временно недоступна',
                'source': 'Youla'  # Исправлено на правильный источник
            }

            # Парсим название
            try:
                result['title'] = item.find_element(
                    By.CSS_SELECTOR,
                    self.selectors['title']
                ).text.strip()
            except NoSuchElementException:
                print(f"Элемент с селектором {self.selectors['title']} не найден.")
                print(self.selectors['title'])
            except InvalidSelectorException:
                print(f"Невалидный селектор: {self.selectors['title']}")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")

            # Парсим цену
            try:
                result['price'] = item.find_element(
                    By.CSS_SELECTOR,
                    self.selectors['price']
                ).text.strip()
            except NoSuchElementException:
                print(f"Элемент с селектором {self.selectors['price']} не найден.")
            except InvalidSelectorException:
                print(f"Невалидный селектор: {self.selectors['price']}")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")

            # Парсим ссылку
            try:
                result['link'] = item.find_element(
                    By.CSS_SELECTOR,
                    self.selectors['link']
                ).get_attribute('href')
            except NoSuchElementException:
                print(f"Элемент с селектором {self.selectors['link']} не найден.")
            except InvalidSelectorException:
                print(f"Невалидный селектор: {self.selectors['link']}")
            except Exception as e:
                print(f"Произошла непредвиденная ошибка: {e}")

            results.append(result)

        return results