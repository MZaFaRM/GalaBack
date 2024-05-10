from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductAPIView.as_view(), name="products"),
    path("save-to-events/", views.AddProductToEvent.as_view(), name="products"),
    path("<str:pk>/", views.ProductAPIView.as_view(), name="products"),
]
