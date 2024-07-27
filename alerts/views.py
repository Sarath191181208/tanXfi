from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Alert
from .serializers import AlertSerializer
import redis

# Setup Redis
# cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class Cache:
    def __init__(self) -> None:
        ...
    def get(self, _: str):
        return None 
    def set(self, timeout: int, *_):
        return None
cache = Cache()


class AlertCreateView(generics.CreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AlertDeleteView(generics.DestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Alert.objects.get(id=self.kwargs['pk'], user=self.request.user)
        obj.status = 'deleted'
        obj.save()
        return obj

class AlertListView(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_filter = self.request.query_params.get('status')
        queryset = Alert.objects.filter(user=self.request.user)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def list(self, request, *args, **kwargs):
        cache_key = f"alerts_{request.user.id}_{request.query_params.get('status', 'all')}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*5)  # Cache for 5 minutes
        return response
