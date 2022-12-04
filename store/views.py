from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from .models import *
from .seriallizers import *
from .filters import ProductFilter
from .pagination import DefaultPagination
# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    filterset_class = ProductFilter
    search_fields = ['title', 'description',]
    ordering_fields = ['unit_price', 'last_update']    
        
    def get_serializer_context(self):
        return {"request": self.request}
    
    def destroy(self, request, *args, **kwargs): 
        if OrderItem.objects.filter(product_id= kwargs['pk']).count() > 0:
            return Response({"error": "Product cannot be deleted."})      
        return super().destroy(request, *args, **kwargs)    
    
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
            product_count=Count('products')).all()
    serializer_class = CollectionSerializer
    

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.annotate(
            product_count=Count('products')).count()> 0:
            return Response({"error": "due to the products that are in this collection, this operation can't be done."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
        
        
class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin,
                  DestroyModelMixin, 
                  GenericViewSet ):
    
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
    
class CartItemsViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateClassItemSerializer
        
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
        
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])\
            .select_related('product')