from django.urls import path
from .views import *

urlpatterns = [
    path(
        "transcriptions/",
        UserTranscriptionListView.as_view(),
        name="user-transcriptions",
    ),
    path(
        "<uuid:audio_id>/transcription/",
        AudioTranscriptionView.as_view(),
        name="audio-transcription-create",
    ),
]
