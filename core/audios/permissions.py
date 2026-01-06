from rest_framework.permissions import BasePermission
from audios.models import Audio


class IsAudioOwner(BasePermission):
    
    def has_permission(self, request, view):
        audio_id = (
            view.kwargs.get("audio_id")
            or view.kwargs.get("id")
        )

        if not audio_id:
            return True

        return Audio.objects.filter(
            id=audio_id,
            user=request.user,
            is_deleted=False,
        ).exists()

class IsAudioOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET",):
            return True

        audio_id = view.kwargs.get("audio_id")
        return Audio.objects.filter(
            id=audio_id,
            user=request.user,
            is_deleted=False,
        ).exists()

