import uuid
from django.db import models
from django.conf import settings
from audios.models import *

class Transcription(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transcriptions",
    )
    
    audio = models.OneToOneField(
        Audio,
        on_delete=models.CASCADE,
        related_name="transcription",
    )

    text = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    progress = models.PositiveSmallIntegerField(default=0)

    language = models.CharField(max_length=10, blank=True)
    model_name = models.CharField(max_length=50, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    processing_time = models.FloatField(null=True, blank=True)  # seconds
    tokens_used = models.PositiveIntegerField(null=True, blank=True)

    error_message = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Transcription #{self.id} ({self.status})"
