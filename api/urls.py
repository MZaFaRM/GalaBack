from django.urls import path, include
from django.urls import path

urlpatterns = [
    path("product/", include("api.products.urls"), name="products"),
    path("event/", include("api.events.urls"), name="events"),
    path("", include("api.user.urls"), name="user"),
]
