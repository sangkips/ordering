from django.urls import path
from . import views

urlpatterns = [
    # path('register/',views.UserView.as_view(),name='register'),
    path(
        "create/customer/", views.CustomerCreateView.as_view(), name="create-customers"
    ),
    path("customers/", views.CustomerViewAll.as_view(), name="customers"),
    path(
        "customers/<int:pk>/", views.CustomerByIdView.as_view(), name="customer-detail"
    ),
]
