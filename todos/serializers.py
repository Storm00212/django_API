from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model that handles conversion between model instances and JSON representation.
    
    This serializer automatically maps the Task model fields to JSON fields for API communication.
    It handles:
    - Serialization: Converting Task model instances to JSON for API responses
    - Deserialization: Converting incoming JSON data to Task model instances for creation/update
    - Validation: Ensuring incoming data meets model constraints before saving
    
    The ModelSerializer class provides default implementations for:
    - create() method for handling POST requests
    - update() method for handling PUT/PATCH requests
    - Field validation based on model field types
    """
    class Meta:
        """
        Meta class that contains metadata options for the serializer.
        """
        model = Task  # The model that this serializer is based on
        fields = ['id', 'title', 'description', 'is_completed', 'created_at']  # Fields to include in the API
        read_only_fields = ['id', 'created_at']  # Fields that cannot be modified via API (auto-generated)