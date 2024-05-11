from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils.response import CustomResponse, HandleException

from ..models import Product, Rating
from . import serializers


class ProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            products = Product.objects.all()
            serializer = serializers.ProductListSerializer(products, many=True)
        else:
            product = Product.objects.get(pk=pk)
            serializer = serializers.ProductSerializer(
                product, context={"request": request}
            )

        return CustomResponse(
            status_code=status.HTTP_200_OK,
            message="Products retrieved successfully",
            data=serializer.data,
        ).to_dict()

    def post(self, request):
        serializer = serializers.ProductSaveSerializer(data=request.data)
        if not serializer.is_valid():
            return HandleException(
                message="Invalid data provided",
                data=serializer.errors,
            ).send_response()
        serializer.save(created_by=request.user)
        return CustomResponse(
            status_code=status.HTTP_201_CREATED,
            message="Product created successfully",
            data=serializer.data,
        ).to_dict()

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return CustomResponse(
                status_code=status.HTTP_204_NO_CONTENT,
                message="Product deleted successfully",
            ).to_dict()
        except Product.DoesNotExist as e:
            return HandleException(
                message="Product does not exist", exception=e
            ).send_response()

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = serializers.ProductSaveSerializer(
                product, data=request.data, partial=True
            )
            if not serializer.is_valid():
                return HandleException(
                    message="Invalid data provided", exception=serializer.errors
                ).send_response()
            serializer.save(created_by=request.user)
            return CustomResponse(
                status_code=status.HTTP_200_OK,
                message="Product updated successfully",
                data=serializer.data,
            ).to_dict()
        except Product.DoesNotExist as e:
            return HandleException(
                message="Product does not exist", exception=e
            ).send_response()


class AddProductToEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.ProductEventSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return HandleException(
                message="Invalid data provided", data=serializer.errors
            ).send_response()
        serializer.save(user=request.user)
        return CustomResponse(
            status_code=status.HTTP_200_OK,
            message="Product added to event successfully",
        ).to_dict()


class RatingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = serializers.RatingSerializer(data=request.data)
        if not serializer.is_valid():
            return HandleException(
                message="Invalid data provided", data=serializer.errors
            ).send_response()
        serializer.save(user=request.user)
        return CustomResponse(
            status_code=status.HTTP_200_OK,
            message="Rating added successfully",
        ).to_dict()

    def delete(self, request):
        try:
            request.user.user_ratings.all().delete()
            return CustomResponse(
                status_code=status.HTTP_200_OK,
                message="Rating deleted successfully",
            ).to_dict()
        except Rating.DoesNotExist as e:
            return HandleException(
                message="Rating does not exist", exception=e
            ).send_response()
