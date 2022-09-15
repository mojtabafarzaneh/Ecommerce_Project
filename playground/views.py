from django.shortcuts import render
from django.http import HttpResponse
from store.models import OrderItem, Product



def say_hello(request):
    query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct())
    
    return render(request, 'hello.html', {'name': 'Moj','products': list(query_set)})
