from django.urls import path
from . import views
urlpatterns = [
    path('products/',views.ProductView.as_view(),name='products'),
    path('product/<int:pk>/',views.ProductDetailView.as_view(),name='prdouct-detail'),
]