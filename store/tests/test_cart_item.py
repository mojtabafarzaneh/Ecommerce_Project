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
def create_cart(api_client, authenticate_staff):
    def do_create_cart():
        authenticate_staff(is_staff=True)
        return api_client.post('/store/carts/')
    return do_create_cart


@pytest.fixture
def create_cart_item(api_client, authenticate_staff):
    def do_create_cart_item(cart, product):
        authenticate_staff(is_staff = True)
        response = api_client.post(f'/store/carts/{cart.id}/items/',{
            'product_id': product.id,
            'quantity': 3
        })
        authenticate_staff(is_staff = False)
        return response 
    return do_create_cart_item

@pytest.mark.django_db
class TestGetCartItem:
    def test_cart_exist_return_200(self, api_client, create_cart):

        create_cart = create_cart()
        for_response = create_cart.data['id']
        response = api_client.get(f'/store/carts/{for_response}/items/')
        
        assert response.status_code == status.HTTP_200_OK
        
        
    def test_cart_items_return_200(self, api_client, create_cart_item):
        cart_id = baker.make(Cart)
        product_id = baker.make(Product)
        
        cart_item = create_cart_item(cart_id, product_id)
        data = cart_item.data['id']
        
        response = api_client.get(f'/store/carts/{cart_id.id}/items/{data}/')
        
        assert response.status_code == status.HTTP_200_OK
@pytest.mark.django_db
class TestCreateItem:
    def test_user_not_allowed_return_401(self, api_client):
        product = baker.make(Product)
        cart = baker.make(Cart)
        response = api_client.post(f'/store/carts/{cart.id}/items/', {
            'product_id': product.id,
            'quantity': 2})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_data_invalid_return_400(self, api_client, authenticate_staff):
        product = baker.make(Product)
        cart = baker.make(Cart)
        authenticate_staff(is_staff=True)
        
        response = api_client.post(f'/store/carts/{cart.id}/items/',{
            'product_id': product.id,
            'quantity': ''
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['quantity'] is not None
    
    def test_data_valid_return_201(self, api_client, authenticate_staff):
        authenticate_staff(is_staff=True)
        product = baker.make(Product)
        cart = baker.make(Cart)
        
        response = api_client.post(f'/store/carts/{cart.id}/items/',{
            'product_id': product.id,
            'quantity': 3
        })
        

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        
@pytest.mark.django_db    
class TestupdateItem:
    def test_data_valid_return_200(self, api_client, create_cart_item, authenticate_staff):
        product_id = baker.make(Product)
        cart_id = baker.make(Cart)
        create_item = create_cart_item(cart_id, product_id)
        data = create_item.data['id']
        response = api_client.patch(f'/store/carts/{cart_id.id}/items/{data}/',{'quantity': 4})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['quantity'] == 4
        
    def test_data_invalid_return_400(self, api_client, create_cart_item):
        product_id = baker.make(Product)
        cart_id = baker.make(Cart)
        
        create_item = create_cart_item(cart_id, product_id)
        data = create_item.data['id']
        
        response = api_client.patch(f'/store/carts/{cart_id.id}/items/{data}/', {'quantity': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['quantity'] is not None
        
        
    
    


        