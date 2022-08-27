from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name="login_user"),
    path('logout/', views.logout_user, name="logout_user"),
    path('forgot-password/', views.forgot_password, name="forgot-password"),
    path('reset-password/', views.reset_password, name ="reset-password"),
]