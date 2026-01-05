from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('audios/', include("audios.urls")),
    path('transcription/', include("transcription.urls")),
    path('users/', include("users.urls")),
]
