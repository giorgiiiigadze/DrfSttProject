from django.urls import path

from .views import *

urlpatterns = [
    path( "<uuid:audio_id>/summarize/", AISummarizeAudioView.as_view(), name="ai-audio-summarize" ),
    path( "summaries/", UserSummarizedAudiosView.as_view(), name="ai-user-summaries" ),
]
