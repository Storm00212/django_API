# Task Management API - Django REST Framework Tutorial

This tutorial demonstrates how to build a production-ready Task Management API using Django REST Framework with a PostgreSQL database.

## 1. Environment & Architecture Setup

### Prerequisites
- Python 3.8+
- PostgreSQL installed and running
- Git (optional but recommended)

### Setup Instructions

```bash
# Create project directory
mkdir task_manager_api && cd task_manager_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install django djangorestframework psycopg2-binary

# Create Django project
django-admin startproject task_manager .

# Create Django app for todos
python manage.py startapp todos
```

## 2. Database Configuration

Edit `task_manager/settings.py` to configure PostgreSQL connection:

```python
import os
from pathlib import Path

# SECURITY: Use environment variables for sensitive data
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

# Database configuration using environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'task_manager_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Add installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',      # Django REST Framework
    'todos',               # Our todos app
]
```

### Environment Variables (Recommended for Production)
Create a `.env` file:
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com localhost 127.0.0.1
DB_NAME=task_manager_db
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432
```

## 3. Data Modeling

Define the `Task` model in `todos/models.py`:

```python
from django.db import models
import uuid

class Task(models.Model):
    """
    Model representing a task/todo item.
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        help_text="Unique identifier for the task"
    )
    title = models.CharField(
        max_length=200,
        help_text="Title of the task"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the task"
    )
    is_completed = models.BooleanField(
        default=False,
        help_text="Completion status of the task"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when task was created"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Newest tasks first
```

After defining the model, create and apply migrations:
```bash
python manage.py makemigrations todos
python manage.py migrate
```

## 4. Serialization Layer

Create serializers in `todos/serializers.py`:

```python
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model that handles conversion between 
    model instances and JSON representation.
    """
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']  # These fields are auto-generated
```

## 5. API View Logic

Implement views in `todos/views.py` using ModelViewSet:

```python
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Task model.
    Automatically provides list, create, retrieve, update, and delete actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

Configure URLs in `task_manager/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todos.views import TaskViewSet

# Create router and register our viewset
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # All API endpoints under /api/
]
```

### API Endpoints Provided
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Retrieve a specific task
- `PUT /api/tasks/{id}/` - Update a specific task
- `PATCH /api/tasks/{id}/` - Partially update a specific task
- `DELETE /api/tasks/{id}/` - Delete a specific task

## 6. Project Structure Overview

```
task_manager_api/
├── manage.py                 # Django management script
├── task_manager/             # Project configuration package
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── todos/                   # Todos application
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── migrations/          # Database migrations
│   ├── models.py            # Data models (Task model)
│   ├── serializers.py       # Serialization classes
│   ├── views.py             # View logic (TaskViewSet)
│   └── tests.py             # Unit tests
├── venv/                    # Virtual environment
└── requirements.txt         # Python dependencies (optional)
```

## Running the Development Server

```bash
# Apply database migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The API will be available at:
- Admin interface: http://127.0.0.1:8000/admin/
- API endpoints: http://127.0.0.1:8000/api/tasks/

## Testing the API

You can test the API using:
1. **curl** commands
2. **Postman** or **Insomnia**
3. **Django REST Framework's browsable API** (visit http://127.0.0.1:8000/api/tasks/ in your browser)

### Example curl commands:
```bash
# List all tasks
curl http://127.0.0.1:8000/api/tasks/

# Create a new task
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Django", "description": "Study Django REST Framework"}'

# Get a specific task (replace {id} with actual ID)
curl http://127.0.0.1:8000/api/tasks/{id}/

# Update a task
curl -X PUT http://127.0.0.1:8000/api/tasks/{id}/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn DRF", "description": "Master Django REST Framework", "is_completed": true}'

# Delete a task
curl -X DELETE http://127.0.0.1:8000/api/tasks/{id}/
```

## Production Considerations

For production deployment, consider:
1. Using environment variables for all sensitive configuration
2. Setting `DEBUG = False`
3. Configuring proper ALLOWED_HOSTS
4. Using a production WSGI server (Gunicorn, uWSGI)
5. Setting up proper static file serving
6. Implementing authentication and permissions
7. Adding API documentation (Swagger/OpenAPI)
8. Setting up logging and monitoring
9. Using a process manager (systemd, PM2, Docker)
10. Regular database backups

This completes the comprehensive Django REST Framework Task Management API tutorial with full CRUD functionality using PostgreSQL.