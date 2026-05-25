import pytest
import requests
import responses

from jsonschema import validate
from schemas.products_scheme import PRODUCT_SCHEMA

# =====================================================================
# 1. GET METHOD
# =====================================================================

class TestGetProducts:
    """All tests for the GET /products method"""

    @pytest.fixture(scope="class", autouse=True)
    def shared_response(self, base_url):
        return requests.get(f"{base_url}/products", timeout=5)

    def test_01_valid_get_response_status_and_payload(self, shared_response):
        # Step 1 - Check if response status code is correct
        assert shared_response.status_code == 200, f"Status Code should be 200, but currently it is {shared_response.status_code}"

        # Step 2 - Check if response have correct data format
        products = shared_response.json()
        assert isinstance(products, dict), f"Expected a dictionary objects with products, but got {type(products)}"

        # Step 3 - Check if object in response is not empty
        assert len(products) > 0, "The list of products is empty!"

        #Step 4 - Check if products list exists in response, have correct type and is not empty
        products_list = products.get("products")
        assert products_list is not None, "The response does not contain 'products' key!"
        assert isinstance(products_list, list), f"Expected 'products' to be a list, but got {type(products_list)}"
        assert len(products_list) > 0, "The list of products inside the response is empty!"

        # Step 5 - Check if single product exists, have correct type and contain correct data
        first_product = products_list[0]
        assert isinstance(first_product, dict), f"Expected product to be a dictionary, but got {type(first_product)}"
        assert "id" in first_product, "First product missing 'id' key!"
        assert "title" in first_product, "First product missing 'title' key!"

    def test_02_valid_get_response_fields_data_types_and_constraints(self, shared_response):
        # Step 1 - Check if response is valid (to be sure that test can be continued)
        assert shared_response.status_code == 200, "Failed to fetch products for type validation"
        products_list = shared_response.json().get("products", [])
        assert len(products_list) > 0, "No products available to validate types"

        # Step 2 - Take the first product to validate its data contract
        first_product = products_list[0]

        # Step 3 - Validate date types and constraints for each field according to schema
        validate(instance=first_product, schema=PRODUCT_SCHEMA)

# =====================================================================
# 2. POST METHOD
# =====================================================================

class TestPostCreateProduct:
    """All tests for the POST /products/add method"""

    @pytest.fixture(scope="class")
    def new_product_payload(self):
        """Fixture providing a valid product payload for the POST request"""
        return {
            "title": "BMW Pencil",
            "price": 12.99,
            "description": "A luxury pencil inspired by German engineering.",
            "category": "stationery"
        }

    @responses.activate
    def test_05_create_product(self, base_url, new_product_payload):
        # Step 1 - Send POST request to add a new product
        responses.add_passthru(f"{base_url}/products/add")
        response = requests.post(f"{base_url}/products/add", json=new_product_payload, timeout=5)

        # Step 2 - Check if server respond with correct status
        assert response.status_code == 201, f"Status Code should be 201, but currently it is {response.status_code}"

        # Step 3 - Check if response is a dictionary and has generated an ID
        created_product = response.json()
        assert isinstance(created_product, dict), f"Expected product to be a dictionary, but got {type(created_product)}"
        assert "id" in created_product, "The server did not return a new product id!"
        created_id = created_product.get("id") #saved created product id for future

        # Step 4 - Check if values in created product are the same as provided (also confirm if fields are not empty)
        sent_fields_in_response = {key: created_product[key] for key in new_product_payload}
        assert sent_fields_in_response == new_product_payload, f"Data integrity violation! Expected: {new_product_payload}, but server saved: {sent_fields_in_response}"

        # Step 5 - Create mock to simulate that products was added to database
        mocked_database_record = {**new_product_payload, "id": created_id}
        responses.add(
            method=responses.GET,
            url=f"{base_url}/products/{created_id}",
            json=mocked_database_record,
            status=200
        )

        # Step 6 - Get product data generate through mock
        product_data = requests.get(f"{base_url}/products/{created_id}", timeout=5)
        get_response_payload = product_data.json()

        # Step 7 - Compare if date from GET method is same as in POST method
        sent_fields_in_get = {key: get_response_payload[key] for key in new_product_payload}
        assert get_response_payload.get("id") == created_id, f"Id of the product should be equal to '{created_id}', but currently it is {get_response_payload.get('id')}"
        assert sent_fields_in_get == new_product_payload, f"Data in GET method are not the same as provided during product creation"

# =====================================================================
# 3. ERROR HANDLING (NEGATIVE TESTS)
# =====================================================================

class TestProductsErrorHandling:
    """Negative test scenarios for /products endpoint"""

    #GET METHOD TESTS
    @pytest.mark.parametrize(
        "invalid_id, expected_statuses",
        [
            (9999999999999, [404]),
            ("jhfiad", [400, 404]),
            ("-5", [400, 404]),
            ("12.34", [400, 404])
        ],
        ids=[
            "non-existent-huge-id",
            "string-id",
            "negative-id",
            "float-id"
        ]
    )
    def test_03_get_product_with_invalid_id(self, base_url, invalid_id, expected_statuses):
        # Step 1 - GET product using invalid ID
        response = requests.get(f"{base_url}/products/{invalid_id}", timeout=5)

        # Step 2 - Check if server correctly rejects the request with expected HTTP status
        assert response.status_code in expected_statuses, f"For ID '{invalid_id}' expected one of statuses {expected_statuses}, but got {response.status_code}"

        # Step 3 - Check if error response has a correct message
        error_data = response.json()
        assert isinstance(error_data, dict), "Expected error response to be a dictionary"
        assert "message" in error_data, "Error response missing 'message' key"
        assert len(error_data["message"].strip()) > 0, "Error message cannot be empty"
        assert f"Product with id '{invalid_id}' not found" == error_data["message"], f'Error message text is incorrect. Current value: {error_data["message"]}'

# =====================================================================
# 3. BOUNDARY AND EDGE CASES
# =====================================================================

class TestProductsBoundaryCases:
    """Tests scenarios for edge cases, limits, and system boundaries"""

    # GET METHOD TESTS
    @pytest.mark.parametrize(
        "limit, expected_counts",
        [
            (0, "all_items"),
            (1, 1),
            (10, 10),
        ],
        ids=
        [
            "limit-zero-get-all",
            "limit-minimum",
            "limit-standard"
        ]
    )
    def test_04_check_get_products_pagination_limits(self, base_url, limit, expected_counts):
        # Step 1 - GET products using limit parameter
        response = requests.get(f"{base_url}/products/?limit={limit}", timeout=5)
        assert response.status_code == 200, f"Expected 200 OK for limit={limit}, but current status is equal to: {response.status_code}"

        products_list = response.json().get("products", [])

        # Step 2 - Check if list of products contains correct number of items based on provided limit
        if expected_counts == "all_items":
            assert len(products_list) > 0, "Expected all items for limit=0, but the list is empty!"
            assert len(products_list) > 10, f"Expected a full list of items for limit=0, but got only {len(products_list)}"
        else:
            assert len(products_list) == expected_counts, f"Expected {expected_counts} items for limit={limit}, but got {len(products_list)}"