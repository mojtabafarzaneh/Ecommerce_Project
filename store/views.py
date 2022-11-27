from django.shortcuts import render
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .seriallizers import ProductSerializer, CollectionSerializer
from rest_framework import status
# Create your views here.
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        product = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(product,many=True, context={'request':request} )
        data = serializer.data 
        return Response(data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data 
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT','DELETE'])
def product_detail(request, id):
    product = Product.objects.get(pk=id)
    
    if request.method == 'GET':
        try:
            serializer = ProductSerializer(product)
            data = serializer.data 
            return Response(data)   
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data 
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({"error": "object cannot be deleted."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['GET','PUT','DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            product_count=Count('products')
        ), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        data = serializer.data
        return Response(data)
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({"error": "the object cannot be deleted!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(product_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)
        data = serializer.data 
        return Response(data)
    
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        data = serializer.data
        return Response(data,status=status.HTTP_201_CREATED)
        