import time
import io
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def whisper_transcribe(audio):
    start_time = time.time()

    mime_to_ext = {
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/x-wav": "wav",
        "audio/mp4": "mp4",
        "audio/aac": "m4a",
        "audio/ogg": "ogg",
        "audio/flac": "flac",
        "audio/webm": "webm",
        "audio/mpga": "mpga",
    }

    ext = mime_to_ext.get(audio.mime_type, "mp3")

    with audio.file.open("rb") as f:
        data = f.read()

    response = client.audio.transcriptions.create(
        file=(f"audio.{ext}", data),
        model="whisper-1",
        response_format="verbose_json",
    )

    return {
        "text": response.text,
        "language": response.language,
        "confidence": None,
        "tokens_used": None,
        "processing_time": time.time() - start_time,
        "model_name": "whisper-1",
    }
