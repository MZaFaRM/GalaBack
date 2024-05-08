from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.response import CustomResponse, HandleException

from ..models import Event
from .serializers import EventSerializer, GetEventSerializer


class EventAPIView(APIView):
    def get(self, request, pk=None):
        try:
            if pk is None:
                events = Event.objects.all()
                serializer = GetEventSerializer(events, many=True)
                return CustomResponse(
                    status.HTTP_200_OK,
                    "Events retrieved successfully",
                    data=serializer.data,
                ).to_dict()
            else:
                event = Event.objects.get(pk=pk)
                serializer = GetEventSerializer(event)
                return CustomResponse(
                    status.HTTP_200_OK,
                    "Event retrieved successfully",
                    data=serializer.data,
                ).to_dict()
        except Event.DoesNotExist as e:
            return HandleException(
                "Event not found", data=None, exception=e
            ).send_response()

    def post(self, request):
        try:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                event = serializer.save()
                return CustomResponse(
                    status.HTTP_201_CREATED, "Event created successfully", data=event.pk
                ).to_dict()
            return CustomResponse(
                status.HTTP_400_BAD_REQUEST,
                "Failed to create event",
                error=serializer.errors,
            ).to_dict()
        except Exception as e:
            return HandleException(
                message="Failed to create event", data=None, exception=e
            ).send_response()

    def patch(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse(
                    status.HTTP_200_OK,
                    "Event updated successfully",
                ).to_dict()
            return CustomResponse(
                status.HTTP_400_BAD_REQUEST,
                "Failed to update event",
                error=serializer.errors,
            ).to_dict()
        except Event.DoesNotExist as e:
            return HandleException(
                "Event not found", data=None, exception=e
            ).send_response()

    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            event.delete()
            return CustomResponse(
                status.HTTP_204_NO_CONTENT, "Event deleted successfully"
            ).to_dict()
        except Event.DoesNotExist as e:
            return HandleException(
                "Event not found", data=None, exception=e
            ).send_response()
