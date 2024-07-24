from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from django.core.cache import cache

from apps.orders.models import Item, Order, OrderDetail
from apps.orders.serializers import (
    OrderCreateSerializer,
    OrderDetailsSerializer,
    ProductCreateSerializer,
)
from apps.orders.sms import make_post_request
# Create your views here.


class ProductView(generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()

        serializer = self.serializer_class(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create an item")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated]

    # Function to get an item by it ID
    @swagger_auto_schema(operation_summary="Get an item by ID")
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)

        serializer = self.serializer_class(instance=item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a function to update the product
    @swagger_auto_schema(operation_summary="Update an item")
    def put(self, request, pk):
        item = get_object_or_404(Item, pk=pk)

        serializer = self.serializer_class(instance=item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()

        serializer = self.serializer_class(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create an order")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewById(generics.GenericAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    @swagger_auto_schema(operation_summary="Get an order by ID")
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        serializer = self.serializer_class(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailsView(generics.GenericAPIView):
    serializer_class = OrderDetailsSerializer
    queryset = OrderDetail.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = OrderDetail.objects.all()

        serializer = self.serializer_class(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create an an order line")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            send_sms = make_post_request()
            if send_sms.status_code == 201:
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrderDetailById(generics.GenericAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get an order line by ID")
    def get(self, request, pk):
        order = get_object_or_404(OrderDetail, pk=pk)

        serializer = self.serializer_class(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderSearchView(generics.GenericAPIView):
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD 00:00:00)",
                type=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="End date (YYYY-MM-DD 00:00:00)",
                type=openapi.FORMAT_DATE,
            ),
        ]
    )
    def get(self, request):
        # filter() with range date fields
        # Ensure its timezone aware
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        
        cache_data = cache.get(f"orders_{start_date}_{end_date}") 

        if start_date and end_date:
            search = OrderDetail.objects.filter(
                created_at__range=[start_date, end_date]
            )
            serializer = self.serializer_class(search, many=True)
            data = serializer.data
            # cache data for a period of 30 days or more depending on your use
            cache.set(cache_data,data, timeout=60 * 60 * 24 * 30)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Both start_date and end_date are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
