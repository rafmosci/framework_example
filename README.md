# Hybrid Test Automation Framework for recruitment purpose - backend & frontend

## Test Strategy Specification

The automation strategy splits testing into two independent layers, ensuring both backend data integrity and a flawless frontend user experience.

### 1. API Testing Strategy (Backend Layer)
The backend suite validates core product management endpoints through integration and contract testing:
* **`GET /products` (Contract Validation):** Verifies response status codes, payload structures, and ensures that data types strictly adhere to the expected contract via `jsonschema`.
* **`POST /products` (Functional & Mock Testing):** Verifies data creation logic. To ensure the test is isolated and independent of live database states, a mocking mechanism (`responses`) is used to simulate database instantiation.
* Test scripts built using Python, pytest and requests

### 2. UI Testing Strategy (Frontend Layer)
The frontend suite focuses on a comprehensive **End-to-End (E2E) regression script**:
* **Full Purchase Pipeline:** Simulates a complete, uninterrupted customer journey—from initial search and result filtering, through cart additions, up to multi-step checkout verification.
* **Data Consistency:** Continuously tracks data across the flow, ensuring that information captured on the product page (like price) matches the final checkout order summary using `pytest.approx`.
* Test scripts build using Python, pytest and Playwright
---

## Project Structure

```text
framework_example/
├── api-tests/                     # API Suite (Backend)
│   ├── schemas/                   # JSON schemas
│   ├── tests/                     # Test scripts (test_products.py)
│   └── requirements.txt
├── frontend-tests/                # UI Suite (Frontend)
│   ├── config/                    # Env configuration
│   ├── pages/                     # Page Object Model classes
│   ├── tests/                     # E2E test scripts (test_checkout.py)
│   └── requirements.txt
└── README.md
```

## How to Run the Tests

Since this project uses a monorepo structure, each test suite must be run from its respective directory using its own virtual environment and dependencies.

### Running API Tests

1. Navigate to the API directory and activate the virtual environment:
```
cd api-tests
# Windows:
python -m venv .venv
.venv\Scripts\activate
# macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Execute the tests:
```
# Run all API tests
pytest tests

# Run tests and generate an HTML report
pytest tests --html=raport.html --self-contained-html
```

### Running UI Tests
1. Navigate to the Frontend directory and activate the virtual environment:
```
cd frontend-tests
# Windows:
python -m venv .venv
.venv\Scripts\activate
# macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
```
2. Install the required dependencies and Playwright:
```
pip install -r requirements.txt
playwright install
```
3. Execute the tests:
```
# Run all API tests
pytest tests
```