from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.ProductAPIView.as_view(), name="products"),
    path("product/<str:product_id>/", views.ProductAPIView.as_view(), name="products"),
]
