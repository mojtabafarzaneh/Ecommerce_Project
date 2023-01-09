from django.urls import path,include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename = 'carts')
router.register('customers', views.CustomerViewSet)

products_router = routers.NestedDefaultRouter(router, 'products',lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup  = 'cart')
carts_router.register('items', views.CartItemsViewSet, basename = 'cart-items')
# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls