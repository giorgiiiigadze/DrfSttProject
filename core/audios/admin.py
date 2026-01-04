from django.contrib import admin
from .models import Audio


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "title",
        "user__email",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)
