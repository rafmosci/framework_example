from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page

        self.search_input = page.get_by_placeholder("Search our catalog")

    def make_a_search(self, search_input: str):
        self.search_input.fill(search_input)
        self.search_input.press("Enter")