from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .forms import CreateUserForm


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        res = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return res


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/home.html"


class Login(LoginView):
    template_name = "accounts/login.html"


class Logout(LogoutView):
    template_name = "base.html"
