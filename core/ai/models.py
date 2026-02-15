from django.db import models
from audios.models import Audio

class AISummary(models.Model):
    audio = models.OneToOneField(
        Audio,
        on_delete=models.CASCADE,
        related_name="ai_summary",
    )

    summary = models.TextField()
    key_points = models.JSONField(default=list)
    tone = models.CharField(max_length=100, blank=True)
    topics = models.JSONField(default=list)

    speakers = models.JSONField(default=list, blank=True)
    action_items = models.JSONField(default=list, blank=True)
    notable_quotes = models.JSONField(default=list, blank=True)

    tokens_used = models.PositiveIntegerField(null=True, blank=True)
    input_tokens = models.PositiveIntegerField(null=True, blank=True)
    output_tokens = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI Summary for audio {self.audio_id}"
