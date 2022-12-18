import time

from playwright.sync_api import sync_playwright, Page

from config import app_config


def find_all_artcies_by_shop_id(shop_id: str):
    with sync_playwright() as p:
        result = []
        browser = p.chromium.launch(headless=app_config.headless)
        page = browser.new_page()
        page.goto("https://www.wildberries.ru/brands/{}".format(shop_id))
        page.wait_for_selector("div.product-card-list")
        product_cards = page.locator("div.product-card")
        for i in range(0, product_cards.count()):
            product_card = product_cards.nth(i)
            article = product_card.locator("a.j-card-link").get_attribute("href").split("/")[4]
            result.append(article)
        return result


def find_items_by_shop_id(shop_id: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=app_config.headless)
        page = browser.new_page()

        page.goto("https://www.wildberries.ru/brands/{}".format(shop_id))
        return parse_items_from_brand(page)

def find_all_articles_by_search_query(q: str):
    with sync_playwright() as p:
        result = []

        browser = p.chromium.launch(headless=app_config.headless)
        page = browser.new_page()

        page.goto("https://wb.ru")
        page.wait_for_selector("div.img-plug")
        page.locator("input#searchInput").type(q)
        page.keyboard.press("Enter")

        page.wait_for_selector("div#catalog_sorter")
        cards = page.locator("div.product-card__wrapper")
        for i in range(0, cards.count()):
            card = cards.nth(i)
            href = card.locator("a.j-card-link").get_attribute("href")
            article = href.split("/")[4]
            result.append(article)
        return result


def find_items_by_search_query(q: str):
    with sync_playwright() as p:
        result = []

        browser = p.chromium.launch(headless=app_config.headless)
        page = browser.new_page()

        page.goto("https://wb.ru")
        page.wait_for_selector("div.img-plug")
        page.locator("input#searchInput").type(q)
        page.keyboard.press("Enter")

        time.sleep(1)

        if "brands" in page.url:
            return parse_items_from_brand(page)
        else:
            page.wait_for_selector("div#catalog_sorter")
            amount = page.locator("div.product-card__wrapper").count()
            hrefs = page.locator("a.j-card-link")
            imgs = page.locator("img.thumbnail")
            titles = page.locator("span.goods-name")
            for i in range(0, amount):
                article = hrefs.nth(i).get_attribute("href").split("/")[4]
                src = imgs.nth(i).get_attribute("src")
                title = titles.nth(i).inner_text()

                v = {
                    "article": article,
                    "src": src,
                    "title": title
                }

                print("{}/{}: {}".format(i, amount, v))

                result.append(v)

            return result


def parse_items_from_brand(page: Page):
    result = []
    page.wait_for_selector("div.product-card-list")

    product_cards = page.locator("div.product-card")
    amount = product_cards.count()
    for i in range(0, amount):
        product_card = product_cards.nth(i)

        article = product_card.locator("a.j-card-link").get_attribute("href").split("/")[4]
        src = product_card.locator("img.thumbnail").get_attribute("src")
        title = product_card.locator("span.goods-name").inner_text()

        v = {
            "article": article,
            "src": src,
            "title": title
        }

        print("{}/{}: {}".format(i, amount, v))

        result.append(v)

    return result
