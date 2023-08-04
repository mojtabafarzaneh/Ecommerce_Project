from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Collection
from .serializers import ProductSerializer, COllectionSerializer

# Create your views here.
@api_view()
def products_list(request):
    query = Product.objects.all()
    serializer = ProductSerializer(query, many=True, context={'request':request})
    return Response(serializer.data)

@api_view()
def products_detail(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    queryset = Collection.objects.get(pk=pk)
    serializer = COllectionSerializer(queryset)
    return Response(serializer.data)