from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('create/', views.UserRegistrationView.as_view(), name='signup'),
    path('<pk>/verify/<token>/', views.UserVerificationView.as_view()),
    path('resend_verify_email/', views.ResendVerifyEmailView.as_view(), name='resend'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()), name='profile_update'),
]