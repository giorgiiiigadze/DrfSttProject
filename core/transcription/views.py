from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import *

from audios.models import Audio
from .models import Transcription
from .serializers import TranscriptionSerializer
from .tasks import process_transcription
from .permissions import (
    IsAudioOwner,
    CanCreateTranscription,
)


class UserTranscriptionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TranscriptionSerializer

    def get_queryset(self):
        return (
            Transcription.objects
            .filter(user=self.request.user)
            .select_related("audio")
            .order_by("-created_at")
        )


class AudioTranscriptionView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAudioOwner,
        CanCreateTranscription,
    ]

    def get(self, request, audio_id):
        audio = Audio.objects.select_related("transcription").get(id=audio_id)

        if not hasattr(audio, "transcription"):
            return Response(
                {"detail": "Transcription does not exist yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TranscriptionSerializer(audio.transcription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, audio_id):
        audio = Audio.objects.get(id=audio_id)

        transcription = Transcription.objects.create(
            user=request.user,
            audio=audio,
            status="processing",
        )

        process_transcription.delay(str(transcription.id))

        serializer = TranscriptionSerializer(transcription)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
