import json
import time

import requests
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

# from ProxyManager import ProxyManager
from locator import YoulaLocator


class YoulaParse:
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
        search_input = self.driver.find_element(*YoulaLocator.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(" ".join(self.items))

        search_button = self.driver.find_element(*YoulaLocator.SEARCH_BUTTON)
        search_button.click()

    # def __paginator(self):
    #     while self.driver.find_elements(*YoulaLocator.NEXT_BTN) and self.count > 0:
    #         self.__parse_page()
    #         self.driver.find_element(*YoulaLocator.NEXT_BTN).click()
    #         self.count -= 1

    def __parse_page(self):
        time.sleep(3)
        titles = self.driver.find_elements(*YoulaLocator.TITLES)
        time.sleep(3)
        # print(titles)
        for title in titles:
            # print(title.get_attribute('outerHTML'))
            # print(title.get_attribute('class'))
            # inner_html = title.get_attribute('innerHTML')
            # print("Вложенный HTML:", inner_html)

            name = title.find_element(*YoulaLocator.NAME).text
            # description = title.find_element(*AvitoLocator.DESCRIPTION).text
            url = "https://youla.ru" + title.find_element(
                *YoulaLocator.URL
            ).get_attribute("href")
            price = title.find_element(*YoulaLocator.PRICE).text
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
        with open("items_youla.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__search_items()
        self.__parse_page()


def check_ip(proxy_list):
    for proxy in proxy_list:
        try:
            response = requests.get(
                "https://google.com", proxies={"http": proxy, "https": proxy}
            )
            print(f"Proxy IP: {response.text.strip()}")
        except requests.RequestException as e:
            print(f"Failed to connect with proxy {proxy}: {e}")


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

    YoulaParse(
        url="https://www.youla.ru",  # работает через раз то может ввести запрос то не может???
        count=2,
        version_main=134,
        items=["iphone 13"],
        proxy_manager=None,
    ).parse()
