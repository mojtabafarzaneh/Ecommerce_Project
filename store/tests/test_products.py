from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
import pytest
from store.models import Product
from django.contrib.auth.models import User


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

@pytest.mark.django_db
class TestCreateProduct:
    def test_user_is_anonymous_returns_401(self, create_product):
        response = create_product({'title':'a', 'price':3.21, 'collection':1, 'inventory':1})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_user_is_not_admin_returns_403(self, api_client, create_product, authenticate):
        authenticate(is_staff=False)
        
        response = create_product({'title':'a', 'price':3.21, 'collection':1, 'inventory':1})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_data_is_invalid_returns_400(self, api_client, create_product, authenticate):
        authenticate(is_staff=True)
        
        response = create_product({'title':'a','slug': '-','price': 1, 'collection':1, 'inventory':1})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        #assert response.data['title'] is not None



        
@pytest.mark.django_db
class TestRetriveProducts:
    def test_if_product_exist_return_200(self, api_client):
        product = baker.make(Product)
        
        response = api_client.get(f'/store/products/{product.id}/')
        
        assert response.status_code == status.HTTP_200_OK

