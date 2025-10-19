from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import ProfileView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
