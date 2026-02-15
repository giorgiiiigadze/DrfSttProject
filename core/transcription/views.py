from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import *
from django.shortcuts import get_object_or_404

from audios.models import Audio
from .models import Transcription
from .serializers import *
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
        audio = get_object_or_404(
            Audio.objects.select_related("transcription"),
            id=audio_id,
            user=request.user,
        )

        if not hasattr(audio, "transcription"):
            return Response(
                {
                    "status": "not_created",
                    "progress": 0,
                },
                status=status.HTTP_200_OK,
            )

        transcription = audio.transcription

        if transcription.status in ("pending", "processing"):
            return Response(
                {
                    "status": transcription.status,
                    "progress": transcription.progress,
                },
                status=status.HTTP_200_OK,
            )

        if transcription.status == "failed":
            return Response(
                {
                    "status": "failed",
                    "error_message": transcription.error_message,
                },
                status=status.HTTP_200_OK,
            )

        serializer = TranscriptionSerializer(transcription)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, audio_id):
        audio = get_object_or_404(
            Audio,
            id=audio_id,
            user=request.user,
        )

        transcription, created = Transcription.objects.get_or_create(
            audio=audio,
            defaults={
                "user": request.user,
                "status": "pending",
                "progress": 0,
            },
        )

        if not created and transcription.status in ("pending", "processing"):
            return Response(
                {
                    "status": transcription.status,
                    "progress": transcription.progress,
                },
                status=status.HTTP_202_ACCEPTED,
            )


        if transcription.status == "completed":
            return Response(
                {
                    "detail": "Transcription already completed.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        transcription.status = "pending"
        transcription.progress = 0
        transcription.error_message = None
        transcription.save(update_fields=["status", "progress", "error_message"])

        process_transcription.delay(str(transcription.id))

        return Response(
            {
                "status": "pending",
                "progress": 0,
            },
            status=status.HTTP_202_ACCEPTED,
        )

class EditTranscriptionView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAudioOwner,
    ]

    def get(self, request, audio_id):
        audio = get_object_or_404(
            Audio.objects.select_related("transcription"),
            id=audio_id,
            user=request.user,
        )

        if not hasattr(audio, "transcription"):
            return Response(
                {"detail": "Transcription does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        transcription = audio.transcription
        serializer = TranscriptionSerializer(transcription)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, audio_id):
        audio = get_object_or_404(
            Audio.objects.select_related("transcription"),
            id=audio_id,
            user=request.user,
        )

        if not hasattr(audio, "transcription"):
            return Response(
                {"detail": "Transcription does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        transcription = audio.transcription

        if transcription.status != "completed":
            return Response(
                {"detail": "Transcription is not completed yet."},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = TranscriptionEditSerializer(
            transcription,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class RetranscribeAudioView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAudioOwner,
    ]

    def get(self, request, audio_id):
        audio = get_object_or_404(
            Audio.objects.select_related("transcription"),
            id=audio_id,
            user=request.user,
        )

        if not hasattr(audio, "transcription"):
            return Response(
                {"detail": "Transcription does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        transcription = audio.transcription
        serializer = TranscriptionSerializer(transcription)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, audio_id):
        audio = get_object_or_404(
            Audio.objects.select_related("transcription"),
            id=audio_id,
            user=request.user,
        )

        if not hasattr(audio, "transcription"):
            return Response(
                {"detail": "Transcription does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        transcription = audio.transcription

        transcription.text = ""
        transcription.status = "pending"
        transcription.progress = 0
        transcription.error_message = None
        transcription.completed_at = None
        transcription.save()

        audio.status = "uploaded"
        audio.transcripted = False
        audio.save(update_fields=["status", "transcripted"])

        process_transcription.delay(str(transcription.id))

        return Response(
            {
                "status": "pending",
                "progress": 0,
                "detail": "Re-transcription started. Previous edits will be overwritten.",
            },
            status=status.HTTP_202_ACCEPTED,
        )
