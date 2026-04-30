from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Task model.
    
    This ViewSet automatically provides the following actions:
    - list(): GET /api/tasks/ - Returns a list of all tasks
    - create(): POST /api/tasks/ - Creates a new task
    - retrieve(): GET /api/tasks/{id}/ - Returns a single task
    - update(): PUT /api/tasks/{id}/ - Updates a task (full update)
    - partial_update(): PATCH /api/tasks/{id}/ - Partially updates a task
    - destroy(): DELETE /api/tasks/{id}/ - Deletes a task
    
    The ModelViewSet combines the logic of:
    - ListModelMixin (for list action)
    - CreateModelMixin (for create action)
    - RetrieveModelMixin (for retrieve action)
    - UpdateModelMixin (for update action)
    - DestroyModelMixin (for destroy action)
    - GenericViewSet (base class that provides the viewset behavior)
    
    Attributes:
        queryset: The set of Task objects to operate on (all tasks by default)
        serializer_class: The serializer class to use for data validation and conversion
    """
    # QuerySet that defines which objects will be available in the API
    # Task.objects.all() returns all Task objects from the database
    queryset = Task.objects.all()
    
    # Serializer class responsible for converting Task instances to/from JSON
    serializer_class = TaskSerializer