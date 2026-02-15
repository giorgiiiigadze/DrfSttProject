from rest_framework import serializers
from audios.models import Audio
from ai.models import AISummary

class AudioSummaryListSerializer(serializers.ModelSerializer):
    audio_id = serializers.IntegerField(source="audio.id")

    class Meta:
        model = AISummary
        fields = [
            "audio_id",
            "summary",
            "key_points",
            "topics",
            "tone",
            "speakers",
            "action_items",
            "notable_quotes",
            "tokens_used",
            "input_tokens",
            "output_tokens",
            "created_at",
        ]