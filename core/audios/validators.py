from rest_framework import serializers

MAX_AUDIO_SIZE = 20 * 1024 * 1024
MIN_TITLE_LENGTH = 4

ALLOWED_MIME_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/aac",
    "audio/ogg",
}


def validate_audio_file(file):
    if file.size > MAX_AUDIO_SIZE:
        raise serializers.ValidationError(
            "Audio file is too large. Maximum size is 20 MB."
        )

    content_type = getattr(file, "content_type", None)
    if content_type not in ALLOWED_MIME_TYPES:
        raise serializers.ValidationError(
            "Unsupported audio format."
        )

    return file


def validate_audio_title(value):
    value = value.strip()

    if len(value) < MIN_TITLE_LENGTH:
        raise serializers.ValidationError(
            f"Title must be at least {MIN_TITLE_LENGTH} characters long."
        )

    if value.lower() in {"audio", "recording", "new audio"}:
        raise serializers.ValidationError(
            "Please provide a more descriptive title."
        )

    return value
