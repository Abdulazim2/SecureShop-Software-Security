
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_add_valid_cart_item(client):
    response = client.post(
        "/api/cart/items/",
        json={"product_id": 2, "quantity": 1}
    )

    assert response.status_code == 200
    assert response.json()["items"][0]["quantity"] >= 1


def test_reject_zero_quantity(client):
    response = client.post(
        "/api/cart/items/",
        json={"product_id": 2, "quantity": 0}
    )

    assert response.status_code == 422


def test_reject_negative_quantity(client):
    response = client.post(
        "/api/cart/items/",
        json={"product_id": 2, "quantity": -5}
    )

    assert response.status_code == 422


def test_reject_excessive_quantity(client):
    response = client.post(
        "/api/cart/items/",
        json={"product_id": 2, "quantity": 1001}
    )

    assert response.status_code == 422


def test_reject_nonexistent_product(client):
    response = client.post(
        "/api/cart/items/",
        json={"product_id": 99999, "quantity": 1}
    )

    assert response.status_code == 400


def test_reject_quantity_exceeding_stock(client):
    response = client.post(
        "/api/cart/items/",
        json={"product_id": 2, "quantity": 51}
    )

    assert response.status_code == 400


def test_client_cannot_set_product_price(client):
    response = client.post(
        "/api/cart/items/",
        json={
            "product_id": 2,
            "quantity": 1,
            "price": 0.01,
            "unit_price": 0.01
        }
    )

    assert response.status_code == 200

    item = response.json()["items"][0]

    assert item["unit_price"] == "25.50"
    assert item["line_total"] == "25.50"


def test_sql_injection_search_does_not_expose_products(client):
    payload = "' OR 1=1 --"

    response = client.get(
        "/api/products/search/",
        params={"keyword": payload}
    )

    assert response.status_code == 200
    assert response.json() == []


def test_search_rejects_long_input(client):
    response = client.get(
        "/api/products/search/",
        params={"keyword": "A" * 101}
    )

    assert response.status_code == 422
