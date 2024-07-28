from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateAlertSerializer, ViewAlertSerializer
from .models import Alert


class AlertCreateView(generics.CreateAPIView):
    """
    View to create a new Alert instance.

    Inherits from CreateAPIView to handle POST requests that create a new Alert.
    """
    # Serialize the incoming data to Alert model instance
    serializer_class = CreateAlertSerializer
    
    # Define the permission class to ensure the user is authenticated
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
            Save the Alert instance with the current user set as the 'user' field.
        Args:
            serializer (CreateAlertSerializer): The serializer instance that is being used to create the Alert.
        """
        # Save the Alert instance with the current user set as the 'user' field
        serializer.save(user=self.request.user)


class AlertDeleteView(generics.DestroyAPIView):
    """
    View to delete an Alert instance by marking it as 'deleted'.

    Inherits from DestroyAPIView to handle DELETE requests.
    """
    # Define the permission class to ensure the user is authenticated
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve the Alert instance that the user is authorized to delete.
        Returns:
            Alert: The Alert instance to be (marked as 'deleted') and removed from db.
        Raises:
            NotFound: If the Alert does not exist or the user is not authorized.
        """
        try:
            # Retrieve the Alert instance based on the provided primary key (pk)
            obj = Alert.objects.get(id=self.kwargs["pk"], user=self.request.user)
            
            # Mark the Alert as 'deleted' and save the changes
            obj.status = "deleted"
            obj.save()
            
            # Return the Alert instance to delete in db
            return obj
        except Alert.DoesNotExist:
            # Raise a NotFound exception if the Alert does not exist or the user is not authorized
            raise NotFound(detail="Alert not found or not authorized to delete.")


class AlertListView(generics.ListAPIView):
    """
    View to list Alert instances for the authenticated user.

    Inherits from ListAPIView to handle GET requests for listing alerts.
    """
    # Incoming data is serialized to Alert model instances
    serializer_class = ViewAlertSerializer
    
    # Define the permission class to ensure the user is authenticated
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the queryset of Alert instances based on the request parameters.

        Filters alerts based on the 'status' query parameter if provided.

        Returns:
            QuerySet: A queryset of Alert instances filtered by the user's alerts 
                      and optional status filter.
        """
        # Get the 'status' filter from the query parameters
        status_filter = self.request.query_params.get("status")
        
        # Filter alerts based on the status if provided, otherwise get all alerts
        if status_filter:
            queryset = Alert.objects.filter(
                user=self.request.user, status=status_filter
            )
        else:
            queryset = Alert.objects.filter(user=self.request.user)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests for listing alerts, with optional caching.

        Returns:
            Response: A Response object containing the serialized list of alerts.
        """
        # Uncomment and adjust cache logic as needed for your caching strategy
        # cache_key = f"alerts_{request.user.id}_{request.query_params.get('status', 'all')}"
        # cached_data = cache.get(cache_key)
        
        # If cached data exists, return it as the response
        # if cached_data:
        #     return Response(cached_data)
        
        # Otherwise, proceed with the standard list view processing
        response = super().list(request, *args, **kwargs)
        
        # Uncomment and adjust caching logic as needed for your caching strategy
        # cache.set(cache_key, response.data, timeout=60*5)  # Cache for 5 minutes
        
        return response
