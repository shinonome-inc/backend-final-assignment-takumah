from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse_lazy

from accounts.models import User


class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test01", email="test@example.com", password="test_0123"
        )

    def test_success_get(self):
        res = self.client.get(reverse_lazy("accounts:login"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "accounts/login.html")

    def test_success_post(self):
        res = self.client.post(
            reverse_lazy("accounts:login"),
            {"username": "test01", "password": "test_0123"},
        )
        self.assertRedirects(res, reverse_lazy("accounts:home"))
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        res = self.client.post(
            reverse_lazy("accounts:login"),
            {"username": "test02", "password": "test_0123"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertFormError(
            res,
            "form",
            None,
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        res = self.client.post(
            reverse_lazy("accounts:login"),
            {"username": "test01", "password": "fail_0123"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertFormError(
            res,
            "form",
            None,
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )
        self.assertNotIn(SESSION_KEY, self.client.session)
