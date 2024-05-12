from typing import Iterable
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = "mobile"
    mobile = models.CharField(unique=True, max_length=10)

    REQUIRED_FIELDS = ["username", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.mobile}"


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    company_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    validated = models.BooleanField(default=False)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_quantity = models.IntegerField()
    mobile = models.CharField(max_length=10)
    chat = models.CharField(max_length=10)
    image = models.ImageField(upload_to="product_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} by {self.company_name}"


class Rating(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_ratings")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_ratings")
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.rating}* {self.comment}"


class UserProductLink(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="pending")
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} by {self.user.first_name}"


class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="event_images/")
    notes = models.TextField(blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Todo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data = models.TextField()
    status = models.BooleanField(max_length=50, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.first_name
