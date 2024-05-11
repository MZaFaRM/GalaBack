import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from django.db.models import Avg
from ..models import Product, Rating, UserProductLink


class ProductSaveSerializer(serializers.ModelSerializer):
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
    ratings = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "company_name",
            "price",
            "max_quantity",
            "state",
            "district",
            "ratings",
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

    def get_ratings(self, instance):
        ratings = instance.product_ratings.aggregate(Avg("rating", default=0))[
            "rating__avg"
        ]
        peeps = instance.product_ratings.count()
        return {"stars": ratings, "peeps": peeps}


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.first_name", read_only=True)

    def create(self, validated_data):
        Rating.objects.filter(
            user=validated_data["user"], product=validated_data["product"]
        ).delete()
        return super().create(validated_data)

    class Meta:
        model = Rating
        fields = ["id", "rating", "comment", "product", "created_at", "user"]
        extra_kwargs = {"product": {"write_only": True}}


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    ratings = serializers.SerializerMethodField()
    ratings_data = serializers.SerializerMethodField()

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

    def get_ratings(self, instance):
        ratings = instance.product_ratings.aggregate(Avg("rating", default=0))[
            "rating__avg"
        ]
        peeps = instance.product_ratings.count()
        return {"stars": ratings, "peeps": peeps}

    def get_ratings_data(self, instance):
        user = self.context["request"].user
        user_rating = instance.product_ratings.filter(user=user).first()
        other_ratings = instance.product_ratings.exclude(user=user)
        return {
            "user": RatingSerializer(user_rating).data,
            "all": RatingSerializer(other_ratings, many=True).data,
        }

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
            "ratings",
            "ratings_data",
            "image",
        ]
        read_only_fields = ["id"]


class ProductEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProductLink
        fields = ["event", "quantity", "product"]
