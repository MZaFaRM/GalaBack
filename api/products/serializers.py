import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from ..models import Product


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
            encoded_image = data.pop("encoded_image").split(";base64,")[-1]
            decoded_bytes = base64.b64decode(encoded_image)
            data["image"] = ContentFile(decoded_bytes, name="image.jpg")
            super().validate(data)
            return data
        except Exception as e:
            raise serializers.ValidationError(str(e)) from e


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

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
            "image",
        ]
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
