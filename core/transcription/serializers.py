from rest_framework import serializers
from django.utils import timezone

from .models import Transcription
from .validators import (
    validate_language,
    validate_confidence,
    validate_processing_time,
    validate_tokens_used,
    validate_status_transition,
)


class TranscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    language = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[validate_language],
    )

    confidence = serializers.FloatField(
        required=False,
        allow_null=True,
        validators=[validate_confidence],
    )

    processing_time = serializers.FloatField(
        required=False,
        allow_null=True,
        validators=[validate_processing_time],
    )

    tokens_used = serializers.IntegerField(
        required=False,
        allow_null=True,
        validators=[validate_tokens_used],
    )

    class Meta:
        model = Transcription
        fields = [
            "id",
            "user",
            "audio",
            "text",
            "status",
            "language",
            "model_name",
            "confidence",
            "processing_time",
            "tokens_used",
            "error_message",
            "created_at",
            "completed_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "completed_at",
        ]

    def validate_status(self, value):
        instance = self.instance
        validate_status_transition(instance, value)
        return value

    def update(self, instance, validated_data):
        """
        Automatically set completed_at when transcription is completed
        """
        status = validated_data.get("status", instance.status)

        if status == "completed" and instance.completed_at is None:
            validated_data["completed_at"] = timezone.now()

        return super().update(instance, validated_data)
