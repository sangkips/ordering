from rest_framework import serializers

from apps.orders.models import Item, Order, OrderDetail

class OrderCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id']
        
class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        read_only_fields = ['id']
        
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'created_at']
        read_only_fields = ['id']