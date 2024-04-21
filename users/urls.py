from django.urls import path
from .views import user_login, UserRegistrationView, UserProfileView, user_logout, EmailVerificationView

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('logout/', user_logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verify')
]
