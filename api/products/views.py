from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Product
from . import serializers
from utils.response import CustomResponse, HandleException
from utils.exceptions import ValidationError


class ProductAPIView(APIView):
    def get(self, request, pk=None):
        if pk is None:
            products = Product.objects.all()
            serializer = serializers.ProductListSerializer(products, many=True)
        else:
            product = Product.objects.get(pk=pk)
            serializer = serializers.ProductSerializer(product)

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
        serializer.save()
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
            serializer.save()
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
    def post(self, request):
        serializer = serializers.ProductEventSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return HandleException(
                message="Invalid data provided", data=serializer.errors
            ).send_response()
        serializer.save()
        return CustomResponse(
            status_code=status.HTTP_200_OK,
            message="Product added to event successfully",
        ).to_dict()
