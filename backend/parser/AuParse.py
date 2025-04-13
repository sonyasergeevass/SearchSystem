import time
import json

import requests
import undetected_chromedriver as uc
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from ProxyManager import ProxyManager
from locator import AuLocator


class AuParse:
    def __init__(
        self,
        url: str,
        items: list,
        count: int = 10,
        version_main: int = None,
        proxy_manager=None,
    ):
        self.url = url
        self.items = items
        self.count = count
        self.version_main = version_main
        self.data = []
        self.proxy_manager = proxy_manager

    def __set_up(self):
        options = Options()
        # options.add_argument("--headless")  # Запуск браузера в headless режиме

        if self.proxy_manager:
            self.proxy_manager.configure_proxy(options)

        self.driver = uc.Chrome(version_main=self.version_main, options=options)

    def __get_url(self):
        self.driver.get(self.url)
        if "Доступ ограничен" in self.driver.title:
            print("Блок IP")

    def __search_items(self):
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#au-search-form-input'))
        )
        search_input.clear()
        search_input.send_keys(" ".join(self.items))

        search_button = self.driver.find_element(*AuLocator.SEARCH_BUTTON)
        search_button.click()

    def __paginator(self):
        while self.driver.find_elements(*AuLocator.NEXT_BTN) and self.count > 0:
            self.__parse_page()
            self.driver.find_element(*AuLocator.NEXT_BTN).click()
            self.count -= 1

    def __parse_page(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Эмулируем прокрутку с помощью ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(self.driver.find_element(By.TAG_NAME, 'body'))
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()

            # Ждем загрузки новых элементов
            time.sleep(2)  # Увеличьте задержку, если данные загружаются медленно

            # Проверяем, изменилась ли высота страницы
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Если высота не изменилась, выходим из цикла
            last_height = new_height
        titles = self.driver.find_elements(*AuLocator.TITLES)
        for title in titles:
            name = title.find_element(*AuLocator.NAME).text
            # description = title.find_element(*AuLocator.DESCRIPTION).text
            url = title.find_element(*AuLocator.URL).get_attribute("href")
            price = title.find_element(*AuLocator.PRICE).text
            data = {
                "name": name,
                # "description": description,
                "url": url,
                "price": price,
            }
            # if any([item.lower() in description.lower() for item in self.items]):
            self.data.append(data)
            print(data)
        self.__save_data()

    def __save_data(self):
        with open("items_au.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__search_items()
        self.__paginator()


# def check_ip(proxy_list):
#     for proxy in proxy_list:
#         try:
#             response = requests.get(
#                 "https://google.com", proxies={"http": proxy, "https": proxy}
#             )
#             print(f"Proxy IP: {response.text.strip()}")
#         except requests.RequestException as e:
#             print(f"Failed to connect with proxy {proxy}: {e}")


if __name__ == "__main__":
    # proxy_list = [
    #     "http://172.67.181.232:80",
    #     "http://172.67.148.92:80",
    #     "http://50.217.226.46:80",
    #     "http://23.227.38.23:80",
    #
    #
    # ]
    # check_ip(proxy_list)
    # proxy_manager = ProxyManager(proxy_list)

    AuParse(
        url="https://www.au.ru",  # работает через раз то может ввести запрос то не может???
        count=2,
        version_main=134,
        items=["прицеп"],
        proxy_manager=None,
    ).parse()
