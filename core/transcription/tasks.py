from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Transcription
from .services import whisper_transcribe


@shared_task(name="transcriptions.process_transcription")
def process_transcription(transcription_id):
    transcription = Transcription.objects.select_related("audio").get(
        id=transcription_id
    )

    try:
        with transaction.atomic():
            result = whisper_transcribe(transcription.audio)

            transcription.text = result["text"]
            transcription.language = result["language"]
            transcription.model_name = result["model_name"]
            transcription.processing_time = result["processing_time"]
            transcription.tokens_used = result["tokens_used"]
            transcription.status = "completed"
            transcription.completed_at = timezone.now()
            transcription.save()

    except Exception as e:
        transcription.status = "failed"
        transcription.error_message = str(e)
        transcription.save()
        raise
