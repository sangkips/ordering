from django.urls import reverse
from rest_framework.test import APITestCase
from apps.auth_app.models import AuthUser
from rest_framework.test import APIClient


class CustomerCreateViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("create-customers")
        self.valid_user_data = {
            "username": "testuser",
            "password": "testpassword",
            "phone_number": "+254777777777",
            "email": "testuser@example.com",
        }
        self.invalid_user_data = {
            "username": "",
            "password": "testpassword",
            "phone_number": "0777777777",
            "email": "testuser@example.com",
        }

    def test_create_user(self):
        response = self.client.post(self.url, data=self.valid_user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AuthUser.objects.count(), 1)
        self.assertEqual(AuthUser.objects.get().username, "testuser")

    def test_create_user_with_invalid_data(self):
        response = self.client.post(
            self.url, data=self.invalid_user_data, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(AuthUser.objects.count(), 0)

    def test_valid_phone_number(self):
        response = self.client.post(self.url, data=self.valid_user_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AuthUser.objects.get().phone_number, "+254777777777")


class CustomerViewAllTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_all_users(self):
        response = self.client.get(reverse("customers"), format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_fetch_all_users_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("customers"), format="json")
        self.assertEqual(response.status_code, 401)


class CustomerByIdViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_user_by_id(self):
        response = self.client.get(
            reverse("customer-detail", args=[self.user.id]), format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "testuser")

    def test_fetch_user_by_id_without_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse("customer-detail", args=[self.user.id]), format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_fetch_user_by_id_with_invalid_id(self):
        response = self.client.get(
            reverse("customer-detail", args=[999]), format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_fetch_user_by_id_with_invalid_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse("customer-detail", args=[self.user.id]), format="json"
        )
        self.assertEqual(response.status_code, 401)
