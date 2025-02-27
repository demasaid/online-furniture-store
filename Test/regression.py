import pytest
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.services.order_service import OrderService
import pytest
from app.services.auth_service import AuthService
from app.models.user import User
import pytest
from app.models.cart import Cart
from app.models.product import Product
import pytest
from fastapi.testclient import TestClient
from main import app



def test_order_placement():
    """Ensure order processing updates stock and order status correctly."""
    
    # Mock user and product
    user = User(username="customer1", email="customer@example.com")
    product = Product(name="Table", price=100, stock=10)
    
    # Place an order
    order = OrderService.create_order(user, [product])
    
    # Check order status
    assert order.status == "Processing"
    
    # Check stock is reduced
    assert product.stock == 9

    # Ensure order gets updated to 'Completed' when processed
    OrderService.process_order(order)
    assert order.status == "Completed"

def test_user_login():
    """Ensure existing users can still log in after code changes"""
    user = User(username="testuser", password="hashedpassword")
    
    # Verify password works
    assert AuthService.verify_password("hashedpassword", user.password)
    
    # Simulate failed login
    assert not AuthService.verify_password("wrongpassword", user.password)

def test_cart_addition():
    """Ensure adding products to the cart does not break after updates"""
    
    cart = Cart()
    product = Product(name="Chair", price=50)
    
    # Add item to cart
    cart.add_item(product, quantity=1)
    
    assert len(cart.items) == 1
    assert cart.items[0].product.name == "Chair"

def test_cart_removal():
    """Ensure removing items from cart still works after code changes"""
    
    cart = Cart()
    product = Product(name="Chair", price=50)
    
    # Add and remove product
    cart.add_item(product, quantity=2)
    cart.remove_item(product)
    
    assert len(cart.items) == 0


client = TestClient(app)

def test_get_products():
    """Ensure the product list API still works correctly"""
    
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure response is a list
