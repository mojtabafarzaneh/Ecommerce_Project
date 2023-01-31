from rest_framework import status
import pytest 
from model_bakery import baker
from store.models import Customer 



@pytest.mark.django_db
class TestRetriveCustomer:
    def test_user_is_anonymous_return_401(self, api_client):
        
        response = api_client.get('/store/customers/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_user_is_not_admin_return_403(self, api_client, authenticate_staff):
        authenticate_staff(is_staff=False)
        
        response = api_client.get('/store/customers/')
        
        print(response.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_user_is_amin_return_200(self, api_client, authenticate_staff):
        authenticate_staff(is_staff=True)
        
        response = api_client.get('/store/customers/')
        
        assert response.status_code == status.HTTP_200_OK
        