from django.urls import path
from .views import *

urlpatterns = [
    path("api/audios/", Audios.as_view(), name='login'),
    path("api/audios/<uuid:id>/", AudioDetailView.as_view(), name="audio-detail"),
]
