# Django
# Python
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Models
from apps.users.models import CustomUser


class UserTestCase(TestCase):
    def setUp(self):
        user = CustomUser(email="testing_login@api.com", first_name="Testing", last_name="Testing")
        user.set_password("api123$")
        user.save()

    def test_login_user(self):
        client = APIClient()
        url = reverse("token_obtain_pair")
        response = client.post(
            url,
            {
                "email": "testing_login@api.com",
                "password": "api123$",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn("access", result)

    def test_unauthorized_error_user(self):
        client = APIClient()
        url = reverse("auth-get-me")
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        result = json.loads(response.content)
        self.assertIn("detail", result)
