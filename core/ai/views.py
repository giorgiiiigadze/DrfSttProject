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
                "topics": summary.topics,
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

        topics = result.get("topics", [])
        if not isinstance(topics, list):
            topics = []

        key_points = result.get("key_points", [])
        if not isinstance(key_points, list):
            key_points = []

        summary_obj = AISummary.objects.create(
            audio=audio,
            summary=result.get("summary", ""),
            key_points=key_points,
            topics=topics,
            tone=result.get("tone", ""),
            tokens_used=result.get("tokens_used"),
            input_tokens=result.get("input_tokens"),
            output_tokens=result.get("output_tokens"),
        )
        audio.summarized = True
        audio.save(update_fields=['summarized'])

        return Response(
            {
                "summary": summary_obj.summary,
                "key_points": summary_obj.key_points,
                "topics": summary_obj.topics,
                "tone": summary_obj.tone,
                "truncated": truncated,
            },
            status=status.HTTP_200_OK,
        )

class UserSummarizedAudiosView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AudioSummaryListSerializer

    def get_queryset(self):
        return AISummary.objects.filter(
            audio__user=self.request.user,
            audio__is_deleted=False
        ).select_related("audio").order_by("-created_at")