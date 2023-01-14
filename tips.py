from store.models import *
#preload related objects
Product.objects.select_related("...")
Product.objects.prefetch_related("...")

#load only what you need
Product.objects.only('title')
Product.objects.defer('description')

#Use values 
Product.objects.values()
Product.objects.values_list()

# Count Properly
Product.objects.count()

# if you want to update or create lots of objects use:
Product.objects.bulk_create([])
Product.objects.bulk_update([])