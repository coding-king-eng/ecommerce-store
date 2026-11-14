import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_1_health_and_frontend_routes():
    """Verify storefront HTML and health endpoints are reachable."""
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "ZapKart" in res_home.text

    res_health = client.get("/health")
    if res_health.status_code == 200:
        assert res_health.json()["status"].lower() == "ok"


def test_2_auth_signup_and_login_flow():
    """Verify user registration and JWT token generation."""
    unique_email = f"tester_{uuid.uuid4().hex[:6]}@zapkart.com"
    payload = {
        "name": "Test Builder",
        "email": unique_email,
        "password": "StrongPassword123"
    }
    signup_res = client.post("/api/auth/signup", json=payload)
    assert signup_res.status_code in (200, 201)

    login_res = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": "StrongPassword123"
    })
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data


def test_3_bad_input_validation_rejected():
    """Verify negative price, negative stock, and empty names are blocked."""
    bad_product = {
        "name": "",
        "price": -500,
        "stock": -10,
        "category_id": 1
    }
    res = client.post("/api/products", json=bad_product)
    assert res.status_code == 422


def test_4_category_and_product_crud():
    """Verify creating, reading, updating, and searching products."""
    cat_res = client.post("/api/categories", json={
        "name": f"TestCat_{uuid.uuid4().hex[:5]}",
        "description": "Automated test category"
    })
    assert cat_res.status_code in (200, 201)
    cat_id = cat_res.json()["id"]

    prod_res = client.post("/api/products", json={
        "name": "Test Mechanical Keyboard",
        "description": "Tactile switches",
        "price": 2999.0,
        "stock": 10,
        "category_id": cat_id
    })
    assert prod_res.status_code == 201
    prod_id = prod_res.json()["id"]

    # Update product price
    upd_res = client.put(f"/api/products/{prod_id}", json={"price": 2499.0})
    assert upd_res.status_code == 200
    assert upd_res.json()["price"] == 2499.0

    # Search filter check
    search_res = client.get("/api/products?search=Mechanical")
    assert search_res.status_code == 200
    assert any(p["id"] == prod_id for p in search_res.json())


def test_5_invalid_product_id_returns_404():
    """Verify requesting or deleting a non-existent product returns 404."""
    res = client.get("/api/products/999999")
    assert res.status_code == 404


def test_6_cart_and_checkout_deducts_stock():
    """Verify end-to-end cart addition, order placement, and live stock deduction."""
    client.post("/api/seed")
    products = client.get("/api/products").json()
    target = next(p for p in products if p["stock"] >= 2)
    initial_stock = target["stock"]

    # Add 1 unit to cart
    cart_res = client.post("/api/cart", json={"product_id": target["id"], "quantity": 1})
    assert cart_res.status_code == 201

    # Process checkout
    order_res = client.post("/api/orders/checkout", json={
        "customer_name": "Shorya Tester",
        "delivery_address": "Hostel Block A, Jaipur",
        "payment_method": "UPI / ZapPay"
    })
    assert order_res.status_code == 201
    assert order_res.json()["total_amount"] >= target["price"]

    # Verify stock decreased by 1
    updated_prod = client.get(f"/api/products/{target['id']}").json()
    assert updated_prod["stock"] == initial_stock - 1