from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductAPIView.as_view(), name="products"),
    path("review/", views.RatingsAPIView.as_view(), name="ratings"),
    path("review/<str:product_id>/", views.RatingsAPIView.as_view(), name="ratings"),
    path("save-to-events/", views.AddProductToEvent.as_view(), name="products"),
    path("<str:pk>/", views.ProductAPIView.as_view(), name="products"),
]
