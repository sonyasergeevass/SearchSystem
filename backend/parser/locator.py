from selenium.webdriver.common.by import By


class AvitoLocator:
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-marker='search-form/suggest/input']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-marker='search-form/submit-button']")
    NEXT_BTN = (By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']")
    TITLES = (By.CSS_SELECTOR, "[data-marker='item']")
    NAME = (By.CSS_SELECTOR, "[itemprop='name']")
    DESCRIPTION = (By.CSS_SELECTOR, 'div[class*="item-bottom"] > div:first-child p')
    URL = (By.CSS_SELECTOR, "[data-marker='item-title']")
    PRICE = (By.CSS_SELECTOR, "[itemprop='price']")
    # TOTAL_VIEWS = (By.CSS_SELECTOR, "[data-marker='item-view/total-views']")
    # DATE_PUBLIC = (By.CSS_SELECTOR, "[data-marker='item-view/item-date']")
    # SELLER_NAME = (By.CSS_SELECTOR, "[data-marker='seller-info/label']")
    # COMPANY_NAME = (By.CSS_SELECTOR, "[data-marker='seller-link/link']")
    # COMPANY_NAME_TEXT = (By.CSS_SELECTOR, "span")
    # GEO = (By.CSS_SELECTOR, "[class*='style-item-address']")
    # хранить на сервере в json
    # либо в базе хрнаить для каждого сайта json


class YoulaLocator:
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Поиск по объявлениям']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[data-test-action='SearchSubmit']")
    # NEXT_BTN = (By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']")
    TITLES = (By.CSS_SELECTOR, "[data-test-component='ProductOrAdCard']")
    NAME = (By.XPATH, ".//figcaption//span[@data-test-block='ProductName']")
    # DESCRIPTION = (By.CSS_SELECTOR, 'div[class*="item-bottom"] > div:first-child p')
    URL = (By.CSS_SELECTOR, "a[href^='/']")
    PRICE = (By.XPATH, "//span[@data-test-component='Price']")
    # TOTAL_VIEWS = (By.CSS_SELECTOR, "[data-marker='item-view/total-views']")
    # DATE_PUBLIC = (By.CSS_SELECTOR, "[data-marker='item-view/item-date']")
    # SELLER_NAME = (By.CSS_SELECTOR, "[data-marker='seller-info/label']")
    # COMPANY_NAME = (By.CSS_SELECTOR, "[data-marker='seller-link/link']")
    # COMPANY_NAME_TEXT = (By.CSS_SELECTOR, "span")
    # GEO = (By.CSS_SELECTOR, "[class*='style-item-address']")
    # хранить на сервере в json
    # либо в базе хрнаить для каждого сайта json


class AuLocator:
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[name="SearchText"]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'button.au-search-form__submit-button')
    NEXT_BTN = (By.CSS_SELECTOR, 'div.au-micropager__next > a')
    TITLES = (By.CSS_SELECTOR, 'div.au-card-list-item')
    NAME = (By.CSS_SELECTOR, 'div.au-lot-list-card-title a')
    URL = (By.CSS_SELECTOR, 'div.au-lot-list-card-title a')
    PRICE = (By.CSS_SELECTOR, 'span.au-price__value')
    # Описание товара (в данном случае нет явного описания, можно взять категории)
    DESCRIPTION = (By.CSS_SELECTOR, 'div.au-lot-list-card-props a')