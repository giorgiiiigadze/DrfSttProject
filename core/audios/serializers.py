from rest_framework import serializers
from .models import *
from .validators import (
    validate_audio_file,
    validate_audio_title,
)


class AudioSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Audio
        fields = [
            "id",
            "user",
            "file",
            "image",
            "title",
            "duration",
            "size",
            "mime_type",
            "status",
            "transcripted",
            "summarized",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "duration",
            "size",
            "mime_type",
            "status",
            "transcripted",
            "summarized",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

    file = serializers.FileField(
        validators=[validate_audio_file]
    )

    title = serializers.CharField(
        validators=[validate_audio_title]
    )

class AudioNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioNote
        fields = [
            "id",
            "timestamp",
            "text",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
