from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_list ),
    path('products/<int:pk>/', views.products_detail),
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
]
