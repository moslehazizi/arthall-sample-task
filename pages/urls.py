from django.urls import path
from .views import HomePageView, RegisterConfirmationView, UserUpdateView



urlpatterns = [
    path('', HomePageView.as_view(), name='home'), # url of homepage
    path('register-confirmation/', RegisterConfirmationView.as_view(), name='register_confirmation'), # url of page that admin see list of not confirmed artists
    path('user-update/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'), # url for page that admin has access to update each artist and change their confirmation status.
]