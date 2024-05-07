import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    encoded_image = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "company_name",
            "name",
            "description",
            "district",
            "state",
            "price",
            "max_quantity",
            "mobile",
            "chat",
            "encoded_image",
        ]

    def validate(self, data):
        try:
            decoded_bytes = base64.b64decode(data.pop("encoded_image"))
            data["image"] = data["image"] = ContentFile(decoded_bytes, name="image.jpg")
            super().validate(data)
            return data
        except Exception as e:
            raise serializers.ValidationError(str(e))


class ProductListSerializer(serializers.ModelSerializer):
    encoded_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "company_name",
            "description",
            "price",
            "max_quantity",
            "state",
            "district",
            "mobile",
            "chat",
            "encoded_image",
        ]
        read_only_fields = ["id"]

    def get_encoded_image(self, instance):
        if instance.image:
            with instance.image.open("rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
                return encoded_string
        return None
