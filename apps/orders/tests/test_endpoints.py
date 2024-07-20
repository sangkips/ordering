from django.urls import reverse
from rest_framework.test import APITestCase
from apps.auth_app.models import AuthUser
from rest_framework.test import APIClient

from apps.orders.models import Item, Order, OrderDetail

class ProductViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            phone_number="+254777777777",
        )
        self.client.force_authenticate(user=self.user)
        self.item ={
            "name":"test item",
            "price":100 
        }
    
    def test_create_product(self):
        response = self.client.post(reverse("products"), self.item, format="json")
        self.assertEqual(response.status_code, 201)
        
    def test_get_products(self):
        response = self.client.get(reverse("products"), format="json")
        self.assertEqual(response.status_code, 200)
    
    def test_get_products_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("products"), format="json")
        self.assertEqual(response.status_code, 401)
        
    
class ProductDetailViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            phone_number="+254777777777",
        )
        self.data = Item.objects.create(
            name="test item",
            price=100
        )
        self.updated_data = {
            "name":"test item updated",
            "price":200
        }
        self.client.force_authenticate(user=self.user)
        
    def test_get_product_by_id(self):
        self.user.save()
        response = self.client.get(reverse("prdouct-detail", args=[self.data.id]), format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_get_product_by_id_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("prdouct-detail", args=[self.data.id]), format="json")
        self.assertEqual(response.status_code, 401)
        
    def test_update_product(self):
        self.user.save()
        response = self.client.put(reverse("prdouct-detail", args=[self.data.id]), self.updated_data, format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_update_product_by_id_without_authentication(self):
        self.user.save()
        self.client.force_authenticate(user=None)
        response = self.client.put(reverse("prdouct-detail", args=[self.data.id]), self.updated_data, format="json")
        self.assertEqual(response.status_code, 401)

class OrderViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            phone_number="+254777777777",
        )
        self.order={
            "customer": self.user.id,
            "payment_method": "CASH"
        }
        self.client.force_authenticate(user=self.user)
        
    def test_create_order(self):
        response = self.client.post(reverse("orders"), self.order, format="json")
        self.assertEqual(response.status_code, 201)

    def test_get_orders(self):
        response = self.client.get(reverse("orders"), format="json")
        self.assertEqual(response.status_code, 200)
        
    def test_get_orders_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("orders"), format="json")
        self.assertEqual(response.status_code, 401)
        
        
class OrderByIdViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            phone_number="+254777777777",
        )
        self.order= Order.objects.create(
            customer = self.user,
            payment_method = "CASH"
        )
        self.client.force_authenticate(user=self.user)

    def test_get_order_by_id(self):
        response = self.client.get(reverse("order-detail", args=[self.order.id]), format="json")
        self.assertEqual(response.status_code, 200)
        
class OrderDetailViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            phone_number="+254777777777",
        )
        self.data = Item.objects.create(
            name="test item",
            price=100
        )
        self.order= Order.objects.create(
            customer = self.user,
            payment_method = "CASH"
        )
        self.order_detail= {
            "order": self.order.id,
            "item": self.data.id,
            "quantity": 2,
        }
        self.url = reverse("order-line")
        self.client.force_authenticate(user=self.user)
        
    def test_create_order_detail(self):
        response = self.client.post(self.url, self.order_detail, format="json")
        self.assertEqual(response.status_code, 201)

    def test_get_order_detail(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, 200)
        
class OrderDetailByIdViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            phone_number="+254777777777",
        )
       
        self.order= Order.objects.create(
            customer = self.user,
            payment_method = "CASH"
        )
        self.data = Item.objects.create(
            name="test item",
            price=100
        )
        self.order_detail = OrderDetail.objects.create(
            order = self.order,
            item = self.data,
            quantity = 2
        )
       
        self.client.force_authenticate(user=self.user)
        
    def test_get_order_detail_by_id(self):
        response = self.client.get(reverse("order-line-detail", args=[self.order_detail.id]), format="json")
        self.assertEqual(response.status_code, 200)
        