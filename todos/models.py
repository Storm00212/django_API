from django.db import models
import uuid

# Create your models here.
class Task(models.Model):
    """
    Model representing a task/todo item in the system.
    
    Attributes:
        id (UUID): Unique identifier for the task (primary key).
        title (str): Short title or name of the task (max 200 characters).
        description (str): Detailed description of the task (can be blank).
        is_completed (bool): Flag indicating whether the task is completed.
        created_at (datetime): Timestamp when the task was created (auto-set).
    """
    # Using UUID as primary key for better security and scalability
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
        """String representation of the Task model."""
        return self.title

    class Meta:
        """Meta options for the Task model."""
        ordering = ['-created_at']  # Newest tasks first
