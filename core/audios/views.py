from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import *

from .models import *
from .serializer import AudioSerializer

from pydub import AudioSegment

class Audios(ListCreateAPIView):
    serializer_class = AudioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Audio.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get("file")

        duration = None
        if uploaded_file:
            audio = AudioSegment.from_file(uploaded_file)
            duration = len(audio) / 1000

        serializer.save(
            user=self.request.user,
            size=uploaded_file.size,
            mime_type=uploaded_file.content_type,
            duration=duration,
            status="uploaded",
            transcripted=False,
        )

class AudioDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AudioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Audio.objects.filter(user=self.request.user)
