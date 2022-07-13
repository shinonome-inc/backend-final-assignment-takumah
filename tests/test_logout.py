from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse_lazy

from accounts.models import User


class TestLogoutView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test01", email="test@example.com", password="test_0123"
        )

    def test_success_get(self):

        self.client.login(username="test01", password="test_0123")
        self.client.get(reverse_lazy("accounts:logout"))
        self.assertNotIn(SESSION_KEY, self.client.session)
