import httpx

base = "http://127.0.0.1:8000"

with httpx.Client(base_url=base) as client_a, httpx.Client(base_url=base) as client_b:
    # Client A creates a cart item
    add = client_a.post(
        "/api/cart/items/",
        json={"product_id": 2, "quantity": 1}
    )
    print("Client A add:", add.status_code)

    if add.status_code not in (200, 201):
        print(add.text)
        raise SystemExit("Could not create test cart item")

    item_id = add.json()["items"][0]["id"]
    print("Cart item ID:", item_id)

    # Client B attempts unauthorized update
    update = client_b.put(
        f"/api/cart/items/{item_id}",
        json={"quantity": 2}
    )
    print("Client B unauthorized update:", update.status_code)
    print(update.text)

    # Client B attempts unauthorized delete
    delete = client_b.delete(f"/api/cart/items/{item_id}")
    print("Client B unauthorized delete:", delete.status_code)
    print(delete.text)

    # Verify Client A's cart is unchanged
    check = client_a.get("/api/cart/")
    print("Client A cart after attacks:", check.status_code)
    print(check.text)
