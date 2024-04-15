
from django.urls import path
from .views import UserRegistrationView, UserLoginView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("profile/", views.profile, name="profile"),
    path("leaderboad/", views.leaderboad, name="leaderboad"),
    path("quizleaderboard/<int:id>/", views.quizleaderboard, name="quizleaderboard"),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
]