import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']



class Item(BaseModel):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return self.name


class Order(BaseModel):
    PAYMENT_METHOD = (("CASH", "Cash"), ("CARD", "card"), ("MPESA", "mpesa"))

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=25, choices=PAYMENT_METHOD, default=PAYMENT_METHOD[0][0]
    )


    def __str__(self):
        return f"Order by {self.customer.username}"


class OrderDetail(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total = models.FloatField(editable=False)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.item.name
