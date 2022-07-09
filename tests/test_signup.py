from django.test import TestCase
from django.urls import reverse_lazy

from accounts.models import User


class TestSignUpView(TestCase):
    def test_success_get(self):
        res = self.client.get(reverse_lazy("accounts:signup"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "accounts/signup.html")

    def test_success_post(self):
        test_user = {
            "username": "test01",
            "email": "test@example.com",
            "password1": "test_pass_0123",
            "password2": "test_pass_0123",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertRedirects(res, reverse_lazy("accounts:home"))
        user = User.objects.get(username="test01")
        self.assertEqual(user.username, "test01")
        self.assertEqual(user.email, "test@example.com")

    def test_failure_post_with_empty_form(self):
        test_user = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "username", "このフィールドは必須です。")
        self.assertFormError(res, "form", "email", "このフィールドは必須です。")
        self.assertFormError(res, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(res, "form", "password2", "このフィールドは必須です。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_empty_username(self):
        test_user = {
            "username": "",
            "email": "test@example.com",
            "password1": "test_pass_0123",
            "password2": "test_pass_0123",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "username", "このフィールドは必須です。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_empty_email(self):
        test_user = {
            "username": "test01",
            "email": "",
            "password1": "test_pass_0123",
            "password2": "test_pass_0123",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "email", "このフィールドは必須です。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_empty_password(self):
        test_user = {
            "username": "test01",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(res, "form", "password2", "このフィールドは必須です。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_duplicated_user(self):
        test_user = {
            "username": "test01",
            "email": "test@example.com",
            "password1": "test_fail_0123",
            "password2": "test_fail_0123",
        }
        self.client.post(reverse_lazy("accounts:signup"), test_user)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "username", "同じユーザー名が既に登録済みです。")
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_failure_post_with_invalid_email(self):
        test_user = {
            "username": "test01",
            "email": "fail.com",
            "password1": "test_fail_0123",
            "password2": "test_fail_0123",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "email", "有効なメールアドレスを入力してください。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_too_short_password(self):
        test_user = {
            "username": "test01",
            "email": "test@example.com",
            "password1": "0123t",
            "password2": "0123t",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "password2", "このパスワードは短すぎます。最低 8 文字以上必要です。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        test_user = {
            "username": "test02",
            "email": "test@example.com",
            "password1": "test02abc",
            "password2": "test02abc",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "password2", "このパスワードは ユーザー名 と似すぎています。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        test_user = {
            "username": "test03",
            "email": "test@example.com",
            "password1": "80953429156",
            "password2": "80953429156",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "password2", "このパスワードは数字しか使われていません。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_failure_post_with_mismatch_password(self):
        test_user = {
            "username": "test01",
            "email": "test@example.com",
            "password1": "test_pass_0123",
            "password2": "test_fail_0123",
        }
        res = self.client.post(reverse_lazy("accounts:signup"), test_user)
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res, "form", "password2", "確認用パスワードが一致しません。")
        users = User.objects.all()
        self.assertEqual(users.count(), 0)


class TestHomeView(TestCase):
    def test_success_get(self):
        test_user = {
            "username": "test01",
            "email": "test@example.com",
            "password1": "test_pass_0123",
            "password2": "test_pass_0123",
        }
        self.client.post(reverse_lazy("accounts:signup"), test_user)
        res = self.client.get(reverse_lazy("accounts:home"))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "accounts/home.html")
