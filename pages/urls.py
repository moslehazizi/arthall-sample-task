from django.urls import path
from .views import HomePageView, RegisterConfirmationView, UserUpdateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register-confirmation/', RegisterConfirmationView.as_view(), name='register_confirmation'),
    path('user-update/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
]