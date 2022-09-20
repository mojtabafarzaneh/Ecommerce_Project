from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CollectionSerializer, ProductSerializer
from .models import Product, Collection
from store import serializer
# Create your views here.

@api_view()
def product_list(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True, context= {"request": request})    
    return Response(serializer.data)


@api_view()
def product_detail(requesst, id):
    product = Product.objects.get(pk=id)
    serializer = ProductSerializer(product)
    
    return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    collection = Collection.objects.get(pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)