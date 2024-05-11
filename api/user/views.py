from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.response import CustomResponse, HandleException

from .serializer import UserSerializer


class EditProfileView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return CustomResponse(
            status_code=status.HTTP_200_OK,
            message="User updated successfully",
            data=serializer.data,
        ).to_dict()

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return HandleException(
                message="Failed to update user", data=serializer.errors
            ).send_response()

        serializer.save()
        return CustomResponse(
            status_code=status.HTTP_200_OK,
            message="User updated successfully",
            data=serializer.data,
        ).to_dict()


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return HandleException(
                message="Failed to create user", data=serializer.errors
            ).send_response()

        serializer.save()
        return CustomResponse(
            status_code=status.HTTP_201_CREATED,
            message="User created successfully",
            data=serializer.data,
        ).to_dict()


class LoginView(APIView):
    def post(self, request):
        mobile = request.data.get("mobile")
        password = request.data.get("password")
        if user := authenticate(mobile=mobile, password=password):
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            user_data["token"] = token.key
            return CustomResponse(
                status_code=status.HTTP_202_ACCEPTED,
                data=user_data,
                message="Login successful",
            ).to_dict()
        return HandleException(
            message="Invalid mobile number or password"
        ).send_response()
