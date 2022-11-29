from playwright.sync_api import sync_playwright


def find_all_artcies_by_shop_id(shop_id: str):
    with sync_playwright() as p:
        result = []
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.wildberries.ru/brands/{}".format(shop_id))
        page.wait_for_selector("div.product-card-list")
        product_cards = page.locator("div.product-card")
        for i in range(0, product_cards.count()):
            product_card = product_cards.nth(i)
            article = product_card.locator("a.j-card-link").get_attribute("href").split("/")[4]
            result.append(article)
        return result


def find_all_articles_by_search_query(q: str):
    with sync_playwright() as p:
        result = []

        browser = p.chromium.launch(headless=False)
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
