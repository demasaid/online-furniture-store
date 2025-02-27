import pytest
import responses
from fastapi.testclient import TestClient
from main import app
from app.models.user import User
from app.services.auth_service import AuthService

client = TestClient(app)

@pytest.mark.integration
def test_user_registration_and_login():
    """Ensure user can register and log in successfully"""
    
    # Step 1: Register user
    register_response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert register_response.status_code == 201
    assert register_response.json()["message"] == "User created successfully"

    # Step 2: Log in
    login_response = client.post("/login", json={
        "username": "testuser",
        "password": "securepassword"
    })
    assert login_response.status_code == 200
    token = login_response.json().get("token")
    assert token is not None  # Ensure token is received

@pytest.mark.integration
def test_add_product_to_cart():
    """Ensure product is added to the cart and persists in DB"""

    # Step 1: Add a product
    product_response = client.post("/products", json={
        "name": "Laptop",
        "price": 1200
    })
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Step 2: Add product to cart
    cart_response = client.post("/cart", json={
        "product_id": product_id,
        "quantity": 1
    })
    assert cart_response.status_code == 200
    assert cart_response.json()["message"] == "Product added to cart"

    # Step 3: Fetch cart to verify product exists
    fetch_cart = client.get("/cart")
    assert fetch_cart.status_code == 200
    assert len(fetch_cart.json()["items"]) == 1

@pytest.mark.integration
def test_order_processing():
    """Ensure order is created and stock updates correctly"""

    # Step 1: Create a product
    product_response = client.post("/products", json={
        "name": "Phone",
        "price": 800,
        "stock": 10
    })
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    # Step 2: Place an order
    order_response = client.post("/orders", json={
        "product_id": product_id,
        "quantity": 2
    })
    assert order_response.status_code == 200
    order_id = order_response.json()["id"]

    # Step 3: Check if stock is updated
    product_status = client.get(f"/products/{product_id}")
    assert product_status.json()["stock"] == 8  # Stock should be reduced

@pytest.mark.integration
@responses.activate
def test_payment_gateway():
    """Ensure successful payment processing"""
    
    # Mock external API response
    responses.add(
        responses.POST, "https://payment-gateway.com/pay",
        json={"status": "success", "transaction_id": "abc123"}, status=200
    )
    
    # Make API request
    payment_response = client.post("/checkout", json={
        "order_id": 1,
        "amount": 1500
    })
    
    assert payment_response.status_code == 200
    assert payment_response.json()["status"] == "success"
