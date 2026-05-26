import random
import re

from playwright.sync_api import Page

class OrderPage:
    def __init__(self, page: Page):
        self.page = page

        self.proceed_to_checkout_button = page.get_by_role("link", name=re.compile(r"Proceed to checkout", re.IGNORECASE))
        self.firstname_input = page.get_by_label("First name")
        self.lastname_input = page.get_by_label("Last name")
        self.email_input = page.get_by_label("Email")
        self.privacy_checkbox = page.locator("input[name='customer_privacy']")
        self.terms_agree_checkbox = page.locator("input[name='psgdpr']")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.address_input = page.get_by_label("Address", exact=True)
        self.zip_code_input = page.get_by_label("Zip/Postal Code")
        self.city_input = page.get_by_label("City")
        self.identification_number_input = page.get_by_label("Identification number")
        self.pay_by_bank_radio = page.get_by_role("radio", name="Pay by bank wire")
        self.payment_terms = page.locator("input[id='conditions_to_approve[terms-and-conditions]']")
        self.total_price = page.locator(".cart-total .value")
        self.place_order = page.get_by_role("button", name="Place order")
        self.order_confirmed_header = page.get_by_role("heading", name=re.compile(r"Your order is confirmed", re.IGNORECASE))

    def go_to_order(self):
        self.proceed_to_checkout_button.click()

    def select_gender(self, gender):
        self.page.get_by_role("radio", name=gender).check()

    def fill_personal_data_form_data(self, gender, firstname, lastname, email):
        self.select_gender(gender)
        self.firstname_input.fill(firstname)
        self.lastname_input.fill(lastname)
        self.email_input.fill(email)
        self.check_required_terms()
        self.click_continue_button()

    def check_required_terms(self):
        self.privacy_checkbox.check()
        self.terms_agree_checkbox.check()

    def click_continue_button(self):
        self.continue_button.click()

    def fill_address_data_form_data(self, address, zip_code, city, identification_number):
        self.address_input.fill(address)
        self.zip_code_input.fill(zip_code)
        self.city_input.fill(city)
        self.identification_number_input.fill(identification_number)
        self.click_continue_button()

    def choose_bank_payment_method(self):
        self.pay_by_bank_radio.check()

    def accept_order_terms(self):
        self.payment_terms.check()

    def get_total_price_of_order(self):
        total_price = self.total_price.text_content()
        total_price.replace(",", ".")
        match = re.search(r"\d+\.?\d*", total_price)
        if match:
            cleaned_price = match.group()
            return float(str(cleaned_price))
        else:
            raise ValueError(f"Could not extract numeric price from text: '{total_price}'")

    def accept_order(self):
        self.place_order.click()