from django.urls import path
from .views import *

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name='login'),
    path("auth/logout/", LogoutView.as_view(), name='logout'),
    path("auth/refresh/", RefreshView.as_view(), name='refresh-tokens'),

    path("profile/", UserProfileView.as_view(), name='users-profile')
]
