from rest_framework import status
from model_bakery import baker
from store.models import Collection
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollections:
    def test_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({ 'title': 'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
    def test_user_is_not_admin_returns_403(self, api_client, create_collection, authenticate):
        #arange
        authenticate(is_staff=False)
        
        #act
        response = create_collection({ 'title': 'a' })
        
        #assertion
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
    def test_data_is_invalid_returns_400(self, api_client, create_collection, authenticate):
        
        authenticate(is_staff=True)
        
        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_data_is_valid_returns_201(self, api_client, create_collection, authenticate):
        
        authenticate(is_staff=True)
        
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetriveCollection:
    def test_is_collection_exist_return_200(self, api_client):
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title':collection.title,
            
        }