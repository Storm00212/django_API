from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Task model.
    
    WHY THIS MATTERS:
    - Combines all standard CRUD operations (list, create, retrieve, update, destroy) in a single class
    - Reduces code duplication compared to writing separate views for each operation
    - Automatically maps HTTP methods to appropriate actions based on REST conventions
    - Provides consistent API behavior and URL patterns
    - Leverages Django REST Framework's built-in functionality for common patterns
    
    The ViewSet pattern is important because it:
    1. Follows DRY (Don't Repeat Yourself) principles
    2. Ensures consistent implementation of RESTful endpoints
    3. Simplifies URL routing configuration
    4. Makes it easier to maintain and extend the API
    """
    # QuerySet that defines which objects will be available in the API
    # WHY THIS MATTERS:
    # - Determines what data can be accessed through this ViewSet
    # - Task.objects.all() returns all Task objects from the database
    # - Could be filtered to show only user-specific tasks in a multi-user system
    queryset = Task.objects.all()
    
    # Serializer class responsible for converting Task instances to/from JSON
    # WHY THIS MATTERS:
    # - Handles data serialization (model → JSON) for API responses
    # - Handles data deserialization (JSON → model) for API requests
    # - Performs validation on incoming data before saving to database
    # - Controls which fields are exposed in the API (defined in TaskSerializer)
    serializer_class = TaskSerializer