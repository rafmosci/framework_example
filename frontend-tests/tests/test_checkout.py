import pytest
import time
import re

from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchPage
from pages.product_details_page import ProductDetailsPage
from pages.order_page import OrderPage

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
        invalid_items = []
        for item in searched_items_list:
            item_title = search_page.get_product_title_from_searched_list(item).lower()
            if "t-shirt" not in item_title and "tshirt" not in item_title:
                invalid_items.append(item_title)
        assert not invalid_items, f"Found products without 't-shirt' in title: {invalid_items}"

        # Step 4 - Choose first element from the list and add it to cart
        searched_items_list[0].click()
        product_details_page = ProductDetailsPage(page)
        product_price_from_details_page = product_details_page.get_current_product_price()
        product_details_page.click_add_to_chart_button()
        product_details_page.success_modal_dialog.wait_for(state="visible", timeout=10000)
        expect(product_details_page.get_success_modal_label()).to_have_text(re.compile(r"Product successfully added to your shopping cart"))
        product_details_page.click_on_proceed_to_checkout_button()

        # Step 5 - Fill personal details order form
        order_page = OrderPage(page)
        order_page.go_to_order()
        order_page.fill_personal_data_form_data("Mr.", "John", "Test", "j.test@testmail.com")

        # Step 6 -Fill address order data
        order_page.fill_address_data_form_data("Test address", "12345", "Barcelona","987654321")
        order_page.click_continue_button()

        # Step 7 - Check if price in order is same as price in order
        total_price = order_page.get_total_price_of_order()
        assert product_price_from_details_page == pytest.approx(total_price), f"Total price of order is not same as price of selected product, current total price = {total_price}, price of product = {product_price_from_details_page}"

        # Step 8 - Choose payment_method and accept order
        order_page.choose_bank_payment_method()
        order_page.accept_order_terms()
        order_page.accept_order()
        expect(order_page.order_confirmed_header).to_be_visible(timeout=10000)