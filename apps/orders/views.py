from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404

from apps.orders.models import Item, Order, OrderDetail
from apps.orders.serializers import OrderCreateSerializer, OrderDetailsSerializer, ProductCreateSerializer
# Create your views here.

class ProductView(generics.GenericAPIView):
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

    @swagger_auto_schema(operation_summary="Get an order by ID")
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        serializer = self.serializer_class(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderDetailsView(generics.GenericAPIView):
    serializer_class = OrderDetailsSerializer
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
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class OrderDetailById(generics.GenericAPIView):
    serializer_class = OrderDetailsSerializer
    permission_classes = [IsAuthenticated]  
    
    @swagger_auto_schema(operation_summary="Get an order line by ID")   
    def get(self, request, pk):
        order = get_object_or_404(OrderDetail, pk=pk)
        
        serializer = self.serializer_class(instance=order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
