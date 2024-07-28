from rest_framework import serializers
from .models import Alert

class CreateAlertSerializer(serializers.ModelSerializer):
    """
    POST Serializer for creating Alert instances.

    This serializer handles the validation and representation of the data
    required to create a new Alert instance.
    """
    class Meta:
        model = Alert
        fields = ['id', 'target_price']

class ViewAlertSerializer(serializers.ModelSerializer):
    """
    GET Serializer for viewing Alert instances.

    This serializer handles the validation and representation of the data
    for displaying Alert instances with additional details.
    """
    class Meta:
        model = Alert
        fields = ['id', 'coin', 'target_price', 'status']
