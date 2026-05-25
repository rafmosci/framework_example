import pytest
import time

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchPage

class TestE2ECheckout:
    """End-to-End test for the PrestaShop demo store purchase pipeline"""


    def test_01_verify_buy_product_functionality(self, setup_shop):
        # Step 1 - Load shop page and check if url is correct
        page = setup_shop
        expect(page).to_have_url("https://www.blmodules.com/demoshop/en/")

        # Step 2 - Make a search for provided phrase
        home_page = HomePage(page)
        test_search_phrase = ("tshirt")
        home_page.make_a_search(test_search_phrase)

        # Step 3 - Check results of a search (if include correct items)
        search_page = SearchPage(page)
        searched_items_list = search_page.get_list_of_searched_products()
        for item in searched_items_list:
            item_title = search_page.get_product_title_from_searched_list(item).lower()
            assert "t-shirt" in item_title or "tshirt" in item_title, f"Expected 't-shirt' or 'tshirt' to be in product title, but got: '{item_title}'"