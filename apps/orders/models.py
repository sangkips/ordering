from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_METHOD=(
        ('CASH','Cash'),
        ('CARD','card'),
        ('MPESA','mpesa')
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=25, choices=PAYMENT_METHOD, default=PAYMENT_METHOD[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order by {self.customer.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        self.total = self.quantity * self.item.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.item.name