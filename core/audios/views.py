from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Audio, AudioNote
from .serializers import AudioNoteSerializer


from .models import *
from .serializers import *

from pydub import AudioSegment

# Add later to export the audio files transcription

class Audios(ListCreateAPIView):
    serializer_class = AudioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Audio.objects.filter(
            user=self.request.user,
            is_deleted=False
        )
        
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
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Audio.objects.filter(
            user=self.request.user
        )

    def patch(self, request, *args, **kwargs):
        audio = self.get_object()

        if audio.is_deleted:
            return Response(
                {"detail": "Deleted audio is read-only."},
                status=status.HTTP_403_FORBIDDEN
            )

        image = request.FILES.get("image")
        if image:
            audio.image = image
            audio.save(update_fields=["image"])

        serializer = self.get_serializer(audio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        audio = self.get_object()

        if audio.is_deleted:
            return Response(
                {"detail": "Audio already deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        audio.soft_delete()

        return Response(
            {"detail": "Audio deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class DeletedAudiosView(ListAPIView):
    serializer_class = AudioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Audio.objects.filter(
            user=self.request.user,
            is_deleted=True
        )
    
class RestoreAudioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        audio = Audio.objects.filter(
            id=id,
            user=request.user,
            is_deleted=True
        ).first()

        if not audio:
            return Response(
                {"detail": "Deleted audio not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        audio.restore()

        return Response(
            {"detail": "Audio restored successfully."},
            status=status.HTTP_200_OK
        )
    

class AudioNoteListCreateView(ListCreateAPIView):
    serializer_class = AudioNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        audio_id = self.kwargs["audio_id"]

        return AudioNote.objects.filter(
            audio__id=audio_id,
            audio__user=self.request.user
        ).order_by("timestamp")

    def perform_create(self, serializer):
        audio_id = self.kwargs["audio_id"]

        audio = get_object_or_404(
            Audio,
            id=audio_id,
            user=self.request.user,
            is_deleted=False
        )

        serializer.save(
            audio=audio,
            user=self.request.user
        )

class AudioNoteDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AudioNote.objects.filter(
            user=self.request.user
        )
