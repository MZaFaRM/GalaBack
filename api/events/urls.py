from django.urls import path
from . import views

urlpatterns = [
    path("", views.EventAPIView.as_view(), name="events"),
    path("<str:pk>/", views.EventAPIView.as_view(), name="events"),
]
