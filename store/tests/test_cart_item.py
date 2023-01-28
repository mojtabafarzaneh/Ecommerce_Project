from rest_framework import status 
from model_bakery import baker
import pytest
from store.models import Cart, Product, CartItem


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

@pytest.fixture
def create_cart(api_client):
    api_client.post('/store/carts/')
    


@pytest.mark.django_db
class TestGetCartItem:
    def test_if_cart_exist_returns_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        create_cart = api_client.post('/store/carts/')
        for_response = create_cart.data['id']
        response = api_client.get(f'/store/carts/{for_response}/items/')
        
        print(for_response)
        print(response)
        assert response.status_code == status.HTTP_200_OK
    