from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework import status

from .models import *
from .serializers import AudioSerializer

from pydub import AudioSegment

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

    def get_queryset(self):
        return Audio.objects.filter(
            user=self.request.user,
            is_deleted=False
        )

    def destroy(self, request, *args, **kwargs):
        audio = self.get_object()
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