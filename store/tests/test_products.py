from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
import pytest
from store.models import Product, Collection
from django.contrib.auth.models import User
import json


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

@pytest.mark.django_db
class TestCreateProduct:
    def test_user_is_anonymous_returns_401(self, create_product):
        response = create_product({"title": "ss",
                                   "slug": "ss",
                                   "price": 2.0,
                                   "price_with_tax": 2.2,
                                   "collection": 2,
                                   "inventory": 2})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    
    def test_user_is_not_admin_returns_403(self,api_client, create_product , authenticate):
        authenticate(is_staff=False)

        response = create_product({"title": "ss",
                                   "slug": "ss",
                                   "price": 2.0,
                                   "price_with_tax": 2.2,
                                   "collection": 2,
                                   "inventory": 2})
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_data_is_invalid_returns_400(self, api_client, create_product, authenticate):
        authenticate(is_staff=True)
        
        response = create_product({"title": "ss",
                                   "slug": "ss",
                                   "price": 2.0,
                                   'collection': 2,
                                   "inventory": 2})

        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_data_is_valid_returns_201(self, authenticate, api_client, create_product, create_collection):


        
        authenticate(is_staff=True)
        product = baker.make(Product)
        collection = create_collection({'title':'a'})
        
        valid_data = {
            'title': product.title,
            'slug':product.slug,
            'price':product.unit_price,
            'collection': collection.data['id'],
            'inventory': product.inventory
        }
        
        response = create_product(valid_data)
        
        print(response.data)      
        assert response.status_code == status.HTTP_201_CREATED

        
@pytest.mark.django_db
class TestRetriveProducts:
    def test_if_product_exist_return_200(self, api_client):
        product = baker.make(Product)
        
        response = api_client.get(f'/store/products/{product.id}/')
        
        assert response.status_code == status.HTTP_200_OK

