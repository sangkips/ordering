from django.urls import path
from . import views


urlpatterns = [
    path("products/", views.ProductView.as_view(), name="products"),
    path(
        "products/<str:pk>/", views.ProductDetailView.as_view(), name="prdouct-detail"
    ),
    path("orders/", views.OrderView.as_view(), name="orders"),
    path("orders/<str:pk>/", views.OrderViewById.as_view(), name="order-detail"),
    path("orders/detail", views.OrderDetailsView.as_view(), name="order-line"),
    path(
        "orders/detail/<str:pk>/",
        views.OrderDetailById.as_view(),
        name="order-line-detail",
    ),
    path("orders/search", views.OrderSearchView.as_view(), name="order-search"),
]
