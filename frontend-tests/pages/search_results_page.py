from playwright.sync_api import Page

class SearchPage:
    def __init__(self, page: Page):
        self.page = page

        self.list_of_searched_products = page.locator("div.products.row > div")
        self.product_title_on_searched_list = page.locator("h2.product-title")

    def get_list_of_searched_products(self):
        return self.list_of_searched_products.all()

    def get_product_title_from_searched_list(self, found_item):
        return found_item.locator(self.product_title_on_searched_list).text_content()
