from django.urls import path
from .views import *

urlpatterns = [
    path("api/audios/", Audios.as_view(), name='login'),
    path("api/audios/<uuid:id>/", AudioDetailView.as_view(), name="audio-detail"),
    path("api/audios/deleted/", DeletedAudiosView.as_view(), name="deleted-audios"),
    path("api/audios/restore/<uuid:id>/", RestoreAudioView.as_view(), name="restore-audio"),

    path( "api/audios/<uuid:audio_id>/notes/", AudioNoteListCreateView.as_view(), name="audio-notes"),
    path( "api/audios/notes/<int:pk>/", AudioNoteDeleteView.as_view(), name="audio-note-delete"),
]
