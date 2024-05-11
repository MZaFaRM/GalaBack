import base64
import os

from django.core.files.base import ContentFile
from rest_framework import serializers

from ..models import Event, Todo, UserProductLink


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["data", "status"]


class UserProductLinkSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name")
    mobile = serializers.CharField(source="product.mobile")
    chat = serializers.CharField(source="product.chat")
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        if image := instance.product.image:
            with image.open("rb") as img_file:
                image_data = img_file.read()
                encoded_image = base64.b64encode(image_data).decode("utf-8")

                if image.name.endswith(".png"):
                    return f"data:image/png;base64,{encoded_image}"
                elif image.name.endswith(".jpg") or image.name.endswith(".jpeg"):
                    return f"data:image/jpeg;base64,{encoded_image}"
                elif image.name.endswith(".gif"):
                    return f"data:image/gif;base64,{encoded_image}"
                else:
                    return f"data:image/png;base64,{encoded_image}"
        return None

    class Meta:
        model = UserProductLink
        fields = "__all__"


class BaseEventSerializer(serializers.ModelSerializer):
    encoded_image = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Event
        fields = ["id", "name", "description", "notes", "encoded_image"]


class GetEventSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    todos = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_products(self, instance):
        products = UserProductLink.objects.filter(event=instance).order_by("created_at")
        return UserProductLinkSerializer(products, many=True).data

    def get_todos(self, instance):
        todos = Todo.objects.filter(event=instance).order_by("created_at")
        return TodoSerializer(todos, many=True).data

    class Meta:
        model = Event
        read_only_fields = ["id"]
        fields = ["id", "name", "description", "image", "todos", "notes", "products"]

    def get_image(self, instance):
        if instance.image:
            with instance.image.open("rb") as img_file:
                image_data = img_file.read()
                encoded_image = base64.b64encode(image_data).decode("utf-8")

                if instance.image.name.endswith(".png"):
                    return f"data:image/png;base64,{encoded_image}"
                elif instance.image.name.endswith(
                    ".jpg"
                ) or instance.image.name.endswith(".jpeg"):
                    return f"data:image/jpeg;base64,{encoded_image}"
                elif instance.image.name.endswith(".gif"):
                    return f"data:image/gif;base64,{encoded_image}"
                else:
                    return f"data:image/png;base64,{encoded_image}"
        return None


class GetEventListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        read_only_fields = ["id"]
        fields = ["id", "name", "description", "image"]

    def get_image(self, instance):
        if instance.image:
            with instance.image.open("rb") as img_file:
                image_data = img_file.read()
                encoded_image = base64.b64encode(image_data).decode("utf-8")

                if instance.image.name.endswith(".png"):
                    return f"data:image/png;base64,{encoded_image}"
                elif instance.image.name.endswith(
                    ".jpg"
                ) or instance.image.name.endswith(".jpeg"):
                    return f"data:image/jpeg;base64,{encoded_image}"
                elif instance.image.name.endswith(".gif"):
                    return f"data:image/gif;base64,{encoded_image}"
                else:
                    return f"data:image/png;base64,{encoded_image}"
        return None


class BaseProductSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.CharField()

    class Meta:
        fields = ["id", "status"]


class EventSerializer(serializers.Serializer):
    todos = TodoSerializer(many=True)
    event = BaseEventSerializer()
    products = BaseProductSerializer(many=True)

    def create(self, validated_data):
        user = self.context["request"].user

        event = validated_data.pop("event")
        event = Event.objects.create(user=user, **event)

        todos = validated_data.pop("todos")
        for todo in todos:
            Todo.objects.create(user=user, event=event, **todo)
        return event

    def update(self, instance, validated_data):
        user = self.context["request"].user

        event = validated_data.pop("event")

        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

        for key, value in event.items():
            setattr(instance, key, value)

        instance.save()

        todos = validated_data.pop("todos")
        Todo.objects.filter(user=user, event=instance).delete()
        for todo in todos:
            Todo.objects.create(user=user, event=instance, **todo)

        products = validated_data.pop("products")
        for product in products:
            link = UserProductLink.objects.filter(user=user, pk=product["id"])
            if product["status"] != "cancelled":
                link.update(status=product["status"])
            else:
                link.delete()

        return event

    def validate(self, data):
        try:
            encoded_image = data["event"].pop("encoded_image").split(";base64,")[-1]
            decoded_bytes = base64.b64decode(encoded_image)
            data["event"]["image"] = ContentFile(decoded_bytes, name="image.jpg")
            super().validate(data)
            return data
        except Exception as e:
            raise serializers.ValidationError(str(e)) from e

    class Meta:
        fields = ["event", "todos", "products"]
