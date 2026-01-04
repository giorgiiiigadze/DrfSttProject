from rest_framework import serializers
from .models import Audio

MAX_AUDIO_SIZE = 20 * 1024 * 1024  # 20 MB
MIN_TITLE_LENGTH = 5

ALLOWED_MIME_TYPES = [
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/aac",
    "audio/ogg",
]

class AudioSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
            "created_at",
            "updated_at",
        ]

    # Checking for audio file, its min size and file format
    def validate_file(self, file):
        if file.size > MAX_AUDIO_SIZE:
            raise serializers.ValidationError(
                "Audio file is too large. Maximum size is 20 MB."
            )

        if file.content_type not in ALLOWED_MIME_TYPES:
            raise serializers.ValidationError(
                "Unsupported audio format."
            )

        return file

    # Checking for audio title
    def validate_title(self, value):
        value = value.strip()

        if len(value) < MIN_TITLE_LENGTH:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )

        return value

    # Cross-field validation hook. Useful for future rules.
    def validate(self, data):
        file = data.get("file")
        title = data.get("title", "")

        if title.lower() in {"audio", "recording", "new audio"}:
            raise serializers.ValidationError(
                {"title": "Please provide a more descriptive title."}
            )

        return data