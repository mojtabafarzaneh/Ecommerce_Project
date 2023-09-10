from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product, Collection, OrderItem, Review, Cart,CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .filters import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    ordering_fields = ['unit_price']
        
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response({'error': 'this product can not be deleted due to some orderation by costumers.'})
        return super().destroy(request, *args, **kwargs)



class CollectionViewSet(ModelViewSet):
    queryset = queryset = queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection = kwargs['pk']).count() > 0:
            return Response({'error':'this collection can not be deleted due to the products that related to it.'})
        return super().destroy(request, *args, **kwargs)


            
    def delete(self, request,pk):
        collection = get_object_or_404(Collection.objects.annotate(
        porducts_count = Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error':'this collection can not be deleted due to the products that related to it.'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin,
                  GenericViewSet, 
                  RetrieveModelMixin, 
                  DestroyModelMixin):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items__product').all()
    
class CartItemsViewSet(ModelViewSet):
    
    http_method_names = ['get', 'post', 'delete', 'patch']
    
    def get_queryset(self, **kwargs):
        return CartItem.objects.\
            filter(cart_id=self.kwargs['cart_pk']).\
            select_related('product')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    

    
    