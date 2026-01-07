from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from audios.models import Audio
from transcription.models import Transcription
from audios.permissions import IsAudioOwner

from .models import AISummary
from .serializers import AudioSummaryListSerializer
from .services.summarizer import summarize_transcript


class AISummarizeAudioView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsAudioOwner,
    ]

    def get(self, request, audio_id):
        audio = get_object_or_404(
            Audio,
            id=audio_id,
            user=request.user,
        )

        if not hasattr(audio, "ai_summary"):
            return Response(
                {"detail": "Summary has not been generated yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        summary = audio.ai_summary

        return Response(
            {
                "summary": summary.summary,
                "key_points": summary.key_points,
                "tone": summary.tone,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, audio_id):
        audio = get_object_or_404(
            Audio.objects.select_related("transcription"),
            id=audio_id,
        )
        self.check_object_permissions(request, audio)

        try:
            transcription = audio.transcription
        except Transcription.DoesNotExist:
            return Response(
                {"detail": "Transcription does not exist to summarize."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if transcription.status != "completed":
            return Response(
                {"detail": "Transcription is not completed yet."},
                status=status.HTTP_409_CONFLICT,
            )

        if hasattr(audio, "ai_summary"):
            return Response(
                {"detail": "Summary already exists."},
                status=status.HTTP_409_CONFLICT,
            )

        text = transcription.text
        truncated = len(text) > 8000

        result = summarize_transcript(
            user=request.user,
            transcript_text=text[:8000],
        )

        summary_obj = AISummary.objects.create(
            audio=audio,
            summary=result.get("summary", ""),
            key_points=result.get("key_points", []),
            tone=result.get("tone", ""),
            tokens_used=result.get("tokens_used"),
            input_tokens=result.get("input_tokens"),
            output_tokens=result.get("output_tokens"),
        )

        return Response(
            {
                "summary": summary_obj.summary,
                "key_points": summary_obj.key_points,
                "tone": summary_obj.tone,
                "truncated": truncated,
            },
            status=status.HTTP_200_OK,
        )



class UserSummarizedAudiosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AudioSummaryListSerializer

    def get_queryset(self):
        return (
            Audio.objects
            .filter(
                user=self.request.user,
                ai_summary__isnull=False,
                is_deleted=False,
            )
            .select_related("ai_summary")
            .order_by("-ai_summary__created_at")
        )
