from django.test import TestCase
from apps.auth_app.models import AuthUser
from rest_framework.test import APIClient


class UserModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AuthUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="TEST3@GMAIL.COM",
            phone_number="+254777777777",
        )

    def test_user_email_is_normalized(self):
        """Test that a new users email is normalized"""
        email = "TEST3@GMAIL.COM"
        self.assertEqual(self.user.email.lower(), email.lower())

    def test_create_user_without_username(self):
        with self.assertRaises(ValueError) as error:
            AuthUser.objects.create_user(
                username=None,
                password="password123%",
                phone_number="+254777777777",
                email="m@gmail.com",
            )
        self.assertEqual("The username field is required", str(error.exception))

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as error:
            AuthUser.objects.create_user(
                username="testuser",
                password="password123%",
                phone_number="+254777777777",
                email=None,
            )
        self.assertEqual("Please set a valid email", str(error.exception))
