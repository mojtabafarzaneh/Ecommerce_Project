from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .seriallizers import ProductSerializer, CollectionSerializer
from rest_framework import status
# Create your views here.
@api_view()
def product_list(request):
    product = Product.objects.select_related('collection').all()
    serializer = ProductSerializer(product,many=True, context={'request':request} )
    data = serializer.data 
    return Response(data)


@api_view()
def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        data = serializer.data 
        return Response(data)   
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view()
def collection_detail(request, pk):
    query_set = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(query_set)
    data = serializer.data
    
    return Response(data)