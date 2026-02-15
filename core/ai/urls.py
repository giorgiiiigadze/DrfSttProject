from django.urls import path

from .views import *

urlpatterns = [
    path( "audio/<uuid:audio_id>/summarize/", AISummarizeAudioView.as_view(), name="ai-audio-summarize" ),
    path( "audio/summaries/", UserSummarizedAudiosView.as_view(), name="ai-user-summaries" ),
]
