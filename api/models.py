import uuid

from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    company_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_quantity = models.IntegerField()
    mobile = models.CharField(max_length=10)
    chat = models.CharField(max_length=10)
    image = models.ImageField(upload_to="product_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()


class Rating(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()


class UserProductLink(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    quantity = models.IntegerField()


class Note(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()


class Todo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()