import random
import re

from playwright.sync_api import Page

class ProductDetailsPage:
    def __init__(self, page: Page):
        self.page = page

        self.product_price = page.locator("span.current-price-value")
        self.size_dropdown = page.get_by_role("combobox", name="Size")
        self.add_to_cart_button = page.get_by_role("button", name="Add to cart")
        self.success_modal_dialog = page.locator("#blockcart-modal .modal-dialog")
        self.success_modal_label = page.locator("#myModalLabel")
        self.proceed_to_checkout_button = page.get_by_role("link", name=re.compile(r"Proceed to checkout", re.IGNORECASE))

    def get_current_product_price(self):
        return float(str(self.product_price.get_attribute("content")))

    def select_random_product_size(self):
        self.size_dropdown.click()
        available_options = [opt for opt in self.size_dropdown.locator("option").all() if opt.get_attribute("selected") is None]
        chosen_option = random.choice(available_options)
        value_to_select = chosen_option.get_attribute("value")
        self.size_dropdown.select_option(value=value_to_select)

    def click_add_to_chart_button(self):
        self.add_to_cart_button.click()

    def get_success_modal_label(self):
        return self.success_modal_dialog.locator(self.success_modal_label)

    def click_on_proceed_to_checkout_button(self):
        self.proceed_to_checkout_button.click()