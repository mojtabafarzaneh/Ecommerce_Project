from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
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


    