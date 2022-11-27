from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

    
class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source= 'unit_price')
    collection = CollectionSerializer()
    detail_collection = serializers.HyperlinkedRelatedField(
            queryset= Collection.objects.all(),
            view_name='collection-detail',
            source = 'collection'
        )    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'price_with_tax', 'collection', 'detail_collection']
        
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')


    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
        