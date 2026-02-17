from rest_framework import routers
from .views import (UserProfileViewSet, CategoryListAPIView,CategoryDetailAPIView, SubCategoryListAPIView,
                    SubCategoryDetailAPIView, ProductListAPIView,  ProductDetailAPIView, ReviewViewSet,CartViewSet,
                    CartItemViewSet, RegisterView, LogoutView, LoginView )
from django.urls import path, include

router = routers.DefaultRouter()

router.register(r'user', UserProfileViewSet, basename='users')
router.register(r'review', ReviewViewSet , basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>', ProductDetailAPIView.as_view(), name='product_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListAPIView.as_view(), name='sub_category_list'),
    path('sub_category/<int:pk>', SubCategoryDetailAPIView.as_view(), name='sub_category_detail'),
    path('cart/', CartViewSet.as_view(), name='cart_detail'),
    path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_items/<int:pk>', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

]




