from rest_framework import status
import pytest



@pytest.mark.django_db
class TestCreateCart:
    def test_user_not_allowed_returns_405(self, api_client):
        response = api_client.get('/store/carts/')
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_user_allowed_returns_201(self, api_client, authenticate_staff):
        authenticate_staff(is_staff=True) 
        
        response = api_client.post('/store/carts/')
        
        assert response.status_code == status.HTTP_201_CREATED
