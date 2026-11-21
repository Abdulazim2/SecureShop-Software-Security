# SecureShop – Security Testing Report

## 1. Introduction

This report documents the security testing performed on the SecureShop backend during Phase 1. The purpose is to verify that implemented security controls work as expected and that common attacks are properly rejected or mitigated.

Testing included automated tests using Pytest and HTTPX, as well as manual API testing through HTTP requests.

## 2. Testing Environment

| Component | Configuration |
|---|---|
| Operating System | Windows |
| Programming Language | Python 3.12.2 |
| Backend Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Testing Framework | Pytest |
| API Testing | HTTPX / FastAPI TestClient |

## 3. Automated Security Tests

The automated test suite contains nine tests.

| Test Case | Expected Result | Actual Result |
|---|---|---|
| Add valid cart item | Item added successfully | Passed |
| Add zero quantity | Request rejected | Passed |
| Add negative quantity | Request rejected | Passed |
| Add excessive quantity | Request rejected | Passed |
| Add nonexistent product | Request rejected | Passed |
| Exceed available stock | Request rejected | Passed |
| Submit manipulated product price | Server uses database price | Passed |
| SQL Injection search payload | No unauthorized data exposure | Passed |
| Excessively long search input | Request rejected | Passed |

### Automated Test Results

Command executed:

```bash
pytest -v
```

Result:

- Total tests: 9
- Passed: 9
- Failed: 0
- Execution time: 1.44 seconds

All nine automated tests passed successfully.

A Starlette deprecation warning related to the current HTTPX integration was reported. It did not affect the test results.

## 4. Manual Security Testing

### 4.1 SQL Injection Testing

**Test:** Submit SQL injection payloads through the product search endpoint.

Examples:

```text
' OR '1'='1
' OR 1=1 --
admin' --
'; DROP TABLE products; --
```

**Expected Result:** Malicious input must not expose unauthorized product data or modify database tables.

**Observed Result:**
- The tested requests returned empty search results.
- The products table remained available after testing.
- No unauthorized product data was returned.

**Status:** Passed.

### 4.2 Price Manipulation Testing

**Test:** Submit a cart request containing a fake client-side price of `0.01` for a product whose actual database price is `25.50`.

**Expected Result:** The server must ignore the submitted price and use the database value.

**Observed Result:**
- Database unit price: 25.50
- Returned unit price: 25.50
- Quantity