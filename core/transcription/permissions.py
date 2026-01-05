import logging
from rest_framework.permissions import BasePermission
from audios.models import Audio

logger = logging.getLogger(__name__)

class IsAudioOwner(BasePermission):
    message = "You do not have permission to access this audio."

    def has_permission(self, request, view):
        audio_id = view.kwargs.get("audio_id")

        if not audio_id or not request.user.is_authenticated:
            return False

        allowed = Audio.objects.filter(
            id=audio_id,
            user=request.user
        ).exists()

        if not allowed:
            logger.warning(
                "Audio ownership violation",
                extra={
                    "user_id": request.user.id,
                    "audio_id": audio_id,
                    "method": request.method,
                    "path": request.path,
                },
            )

        return allowed


class CanCreateTranscription(BasePermission):
    message = "Transcription already exists for this audio."

    def has_permission(self, request, view):
        if request.method != "POST":
            return True

        audio_id = view.kwargs.get("audio_id")

        if not audio_id:
            return False

        audio = (
            Audio.objects
            .filter(id=audio_id, user=request.user)
            .select_related("transcription")
            .first()
        )

        if not audio:
            return False

        if hasattr(audio, "transcription"):
            logger.info(
                "Duplicate transcription attempt",
                extra={
                    "user_id": request.user.id,
                    "audio_id": audio_id,
                },
            )
            return False

        return True
