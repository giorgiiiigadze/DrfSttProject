from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('audios/', include("audios.urls")),
    path('transcription/', include("transcription.urls")),
    path('users/', include("users.urls")),
    path('ai/', include("ai.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )