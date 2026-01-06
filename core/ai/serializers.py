from rest_framework import serializers
from audios.models import Audio
from ai.models import AISummary


class AudioSummaryListSerializer(serializers.ModelSerializer):
    summary = serializers.CharField(source="ai_summary.summary")
    tone = serializers.CharField(source="ai_summary.tone")

    class Meta:
        model = Audio
        fields = [
            "id",
            "title",
            "summary",
            "tone",
            "created_at",
        ]
