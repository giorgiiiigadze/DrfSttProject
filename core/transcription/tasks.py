from celery import shared_task
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.conf import settings

from .models import Transcription
from .services import whisper_transcribe

import math


User = get_user_model()


def seconds_to_credits(seconds: float) -> int:
    return math.ceil(seconds / settings.SECONDS_PER_CREDIT)


@shared_task(name="transcriptions.process_transcription")
def process_transcription(transcription_id):
    transcription = (
        Transcription.objects
        .select_related("audio", "audio__user")
        .get(id=transcription_id)
    )

    user = transcription.audio.user
    audio = transcription.audio

    required_credits = seconds_to_credits(audio.duration)

    with transaction.atomic():
        user = (
            User.objects
            .select_for_update()
            .get(pk=user.pk)
        )

        if user.credits < required_credits:
            transcription.status = "failed"
            transcription.error_message = "Not enough credits for transcription"
            transcription.save(update_fields=["status", "error_message"])
            return

        user.credits -= required_credits
        user.save(update_fields=["credits"])

    try:
        transcription.status = "processing"
        transcription.progress = 5
        transcription.save(update_fields=["status", "progress"])

        transcription.progress = 30
        transcription.save(update_fields=["progress"])

        result = whisper_transcribe(audio)

        transcription.text = result["text"]
        transcription.language = result["language"]
        transcription.model_name = result["model_name"]
        transcription.processing_time = result["processing_time"]
        transcription.tokens_used = result["tokens_used"]

        transcription.status = "completed"
        transcription.progress = 100
        transcription.completed_at = timezone.now()
        transcription.save()

        audio.refresh_from_db()
        audio.transcripted = True
        audio.save(update_fields=["transcripted"])
        print(f"Audio {audio.id} transcripted set to True")

    except Exception as e:
        with transaction.atomic():
            user = (
                User.objects
                .select_for_update()
                .get(pk=user.pk)
            )
            user.credits += required_credits
            user.save(update_fields=["credits"])

        transcription.status = "failed"
        transcription.error_message = str(e)
        transcription.progress = 0
        transcription.save(update_fields=["status", "error_message", "progress"])

        audio.refresh_from_db()
        audio.transcripted = False
        audio.save(update_fields=["transcripted"])
        print(f"Audio {audio.id} transcripted set to False due to failure")

        raise
