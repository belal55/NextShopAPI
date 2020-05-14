from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from store import view
router = DefaultRouter()

router.register(r'categories', view.CategoryViewSet)
router.register(r'subcategories', view.SubCategoryViewSet)
router.register(r'brands', view.BrandViewSet)
router.register(r'products', view.ProductViewSet)
router.register(r'productsImages', view.ProductImageViewSet)
router.register(r'orders', view.OrderViewSet)
router.register(r'ordersItems', view.OrderItemViewSet)

# urlpatterns = router.urls

urlpatterns = [
    url(r'^', include(router.urls)),
    path('order_by_user/<str:id>/', view.order_by_user, name='order_by_user'),
]

