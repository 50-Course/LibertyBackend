from api.app_auth.views import LoginView, SignUpView
from django.urls import path

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", SignUpView.as_view(), name="register"),
]
