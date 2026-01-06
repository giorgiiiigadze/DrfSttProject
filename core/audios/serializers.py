from rest_framework import serializers
from .models import Audio
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
            "title",
            "duration",
            "size",
            "mime_type",
            "status",
            "transcripted",
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
