from django.urls import path
from .views import *

urlpatterns = [
    path( "audio/transcriptions/", UserTranscriptionListView.as_view(), name="user-transcriptions",),
    path( "audio/<uuid:audio_id>/transcription/", AudioTranscriptionView.as_view(), name="audio-transcription-create",),
    path( "audio/<uuid:audio_id>/overwrite/", EditTranscriptionView.as_view(), name="edit-transcription",),
    path( "audio/<uuid:audio_id>/retranscription/", RetranscribeAudioView.as_view(), name="re-transcription",),
]
