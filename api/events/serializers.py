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

    def get_todos(self, instance):
        todos = Todo.objects.filter(event=instance).order_by("created_at")
        return TodoSerializer(todos, many=True).data

    class Meta:
        model = Event
        fields = ["id", "name", "description", "image", "todos", "notes"]
        read_only_fields = ["id"]

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


class EventSerializer(serializers.Serializer):
    todos = TodoSerializer(many=True)
    products = UserProductLinkSerializer(many=True, read_only=True)
    event = BaseEventSerializer()

    def create(self, validated_data):
        event = validated_data.pop("event")
        event = Event.objects.create(**event)

        todos = validated_data.pop("todos")
        for todo in todos:
            Todo.objects.create(event=event, **todo)
        return event

    def update(self, instance, validated_data):
        event = validated_data.pop("event")

        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

        for key, value in event.items():
            setattr(instance, key, value)

        instance.save()

        todos = validated_data.pop("todos")
        Todo.objects.filter(event=instance).delete()
        for todo in todos:
            Todo.objects.create(event=instance, **todo)     
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
