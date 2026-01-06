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
        transcription.status = "processing"
        transcription.progress = 5
        transcription.save(update_fields=["status", "progress"])

        with transaction.atomic():
            transcription.progress = 30
            transcription.save(update_fields=["progress"])

            result = whisper_transcribe(transcription.audio)

            transcription.text = result["text"]
            transcription.language = result["language"]
            transcription.model_name = result["model_name"]
            transcription.processing_time = result["processing_time"]
            transcription.tokens_used = result["tokens_used"]

            transcription.progress = 100
            transcription.status = "completed"
            transcription.completed_at = timezone.now()
            transcription.save()
    
    except Exception as e:
        transcription.status = "failed"
        transcription.error_message = str(e)
        transcription.progress = 0
        transcription.save(update_fields=["status", "error_message", "progress"])
        raise
