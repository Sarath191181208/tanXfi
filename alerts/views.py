from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import AlertSerializer
from .models import Alert


class AlertCreateView(generics.CreateAPIView):
    # serialize the incoming data to Alert model
    serializer_class = AlertSerializer
    # authorize the user to create an alert
    permission_classes = [IsAuthenticated]
    # Save the user who created the alert
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlertDeleteView(generics.DestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Alert.objects.get(id=self.kwargs["pk"], user=self.request.user)
        obj.status = "deleted"
        obj.save()
        # return the alert object
        return obj


class AlertListView(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = Alert.objects.filter(
                user=self.request.user, status=status_filter
            )
        else:
            queryset = Alert.objects.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        # cache_key = f"alerts_{request.user.id}_{request.query_params.get('status', 'all')}"
        # cached_data = cache.get(cache_key)
        # if cached_data:
        #     return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        # cache.set(cache_key, response.data, timeout=60*5)  # Cache for 5 minutes
        return response
