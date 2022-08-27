from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name="login_user"),
    path('adminlogin/', views.login_admin, name="login_admin"),
    path('logout/', views.logout_user, name="logout_user"),
    path('forgot-password/', views.forgot_password, name="forgot-password"),
    path('reset-password/', views.reset_password, name ="reset-password"),
]