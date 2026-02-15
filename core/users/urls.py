from django.urls import path
from .views import *

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name='login'),
    path("auth/register/", RegisterView.as_view(), name='register'),
    path("auth/logout/", LogoutView.as_view(), name='logout'),
    path("auth/refresh/", RefreshView.as_view(), name='refresh-tokens'),

    path("profile/", ProfileView.as_view(), name="user-profile"),
]
