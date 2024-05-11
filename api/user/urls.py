from django.urls import path
from .views import EditProfileView, SignUpView, LoginView

urlpatterns = [
    path("profile/", EditProfileView.as_view(), name="profile"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
]
